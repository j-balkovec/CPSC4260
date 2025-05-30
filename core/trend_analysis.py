# __name__: Jakob Balkovec
# __class__: CPSC 4260 - Software Refactoring
# __date__: Sun Apr 20th, 2025
#
# __file__: trend_analysis.py
#
# __brief__:
#     This file implements the trend analysis feature.
#     This is done thought a lightweight regression model

import os
# =========
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# =========

import sys
import os
import ast
from pathlib import Path
import numpy as np
from typing import List, Tuple, Dict
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.halstead import _calculate_halstead_metrics, _extract_operators_and_operands
from utils.logger import setup_logger
from utils.utility import _save_to_json
from utils.exceptions import CodeProcessingError

trend_logger = setup_logger(
    name="trend_analysis.py_logger", log_file="trend_analysis.log"
)


def _calculate_cyclomatic_complexity(node: ast.AST) -> int:
    """_summary_

    Args:
        node (ast.AST): The AST node to analyze for cyclomatic complexity.

    Returns:
        int: The cyclomatic complexity of the node.
    """
    if isinstance(node, ast.FunctionDef):
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity
    trend_logger.warning(f"Invalid node type {type(node)} for cyclomatic complexity")
    return -9999


def extract_metrics(file_path: Path) -> Dict[str, float]:
    """_summary_

    Args:
        file_path (Path): The path to the Python file to analyze.

    Returns:
        Dict[str, float]: A dictionary containing the calculated metrics:
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            source_code = file.read()

        tree = ast.parse(source_code)

        lines = _extract_operators_and_operands(source_code)
        halstead_metrics = _calculate_halstead_metrics(lines)

        cyclo_sum = 0
        func_count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                cyclo = _calculate_cyclomatic_complexity(node)
                if cyclo != -9999:
                    cyclo_sum += cyclo
                    func_count += 1
        avg_cyclo = cyclo_sum / func_count if func_count > 0 else 1.0
        if func_count == 0:
            trend_logger.warning(
                f"No functions found in {file_path}, using default cyclomatic complexity"
            )
        return {
            "effort": halstead_metrics.get("E", 0.0),
            "difficulty": halstead_metrics.get("D", 0.0),
            "volume": halstead_metrics.get("V", 0.0),
            "length": halstead_metrics.get("N", 0.0),
            "cyclomatic_complexity": avg_cyclo,
            "loc": len(source_code.splitlines()),
        }
    except Exception as e:
        trend_logger.error(f"Error processing file {file_path}: {e}")
        trend_logger.debug(f"Exception for {file_path.name}: {e}")
        return {}


def collect_metrics(file_paths: List[Path]) -> List[Dict[str, float]]:
    """_summary_

    Args:
        file_paths (List[Path]): A list of file paths to Python files.

    Returns:
        List[Dict[str, float]]: A list of dictionaries containing the metrics for each file.
    """
    metrics_list = []
    for file_path in file_paths:
        if file_path.is_file() and file_path.suffix == ".py":
            metrics = extract_metrics(file_path)
            if isinstance(metrics, dict) and metrics:
                metrics["file"] = file_path.name
                metrics_list.append(metrics)
    return metrics_list


def train_model(
        metrics: List[Dict[str, float]], target: str = "effort"
) -> Tuple[np.ndarray, float]:
    """_summary_

    Args:
        metrics (List[Dict[str, float]]): A list of dictionaries containing the metrics for each file.
        target (str, optional): target on which the model is trained on . Defaults to 'effort'.

    Returns:
        Tuple[np.ndarray, float]: A tuple containing the weights of the trained model and the predicted value for the next file.
    """
    if not metrics:
        trend_logger.error("No metrics to train the model")
        return np.array([]), 0.0
    X = np.array(
        [
            [i, m["loc"], m["cyclomatic_complexity"], m["volume"], m["length"]]
            for i, m in enumerate(metrics)
        ]
    )
    y = np.array([m[target] for m in metrics])
    X_mean = np.mean(X, axis=0)
    X_std = np.std(X, axis=0)
    X_std[X_std == 0] = 1
    X_normalized = (X - X_mean) / X_std
    X_normalized = np.c_[np.ones(X_normalized.shape[0]), X_normalized]
    weights = np.random.randn(X_normalized.shape[1])
    learning_rate = 0.01
    n_iterations = 1000
    m = len(y)
    for _ in range(n_iterations):
        predictions = X_normalized @ weights
        errors = predictions - y
        gradient = (1 / m) * X_normalized.T @ errors
        weights -= learning_rate * gradient
    next_X = np.array([len(metrics), X[-1, 1], X[-1, 2], X[-1, 3], X[-1, 4]])
    next_X_normalized = (next_X - X_mean) / X_std
    next_X_normalized = np.r_[1, next_X_normalized]
    next_pred = next_X_normalized @ weights
    return weights, next_pred


def analyze_trends(file_paths: List[Path]) -> Dict:
    """_summary_

    Args:
        file_paths (List[Path]): A list of file paths to Python files to analyze.

    Returns:
        Dict: A dictionary containing the analysis results, including metrics, statistics, predictions, and chart data.
    """
    metrics = collect_metrics(file_paths)

    if not metrics:
        return {"error": "No valid metrics extracted"}

    stats = {
        "effort": {
            "mean": np.mean([m["effort"] for m in metrics]),
            "std": np.std([m["effort"] for m in metrics]),
        },
        "difficulty": {
            "mean": np.mean([m["difficulty"] for m in metrics]),
            "std": np.std([m["difficulty"] for m in metrics]),
        },
        "volume": {
            "mean": np.mean([m["volume"] for m in metrics]),
            "std": np.std([m["volume"] for m in metrics]),
        },
        "length": {
            "mean": np.mean([m["length"] for m in metrics]),
            "std": np.std([m["length"] for m in metrics]),
        },
        "cyclomatic_complexity": {
            "mean": np.mean([m["cyclomatic_complexity"] for m in metrics]),
            "std": np.std([m["cyclomatic_complexity"] for m in metrics]),
        },
        "loc": {
            "mean": np.mean([m["loc"] for m in metrics]),
            "std": np.std([m["loc"] for m in metrics]),
        },
    }
    weights, next_effort = train_model(metrics, target="effort")
    chart_data = {
        "labels": [m["file"] for m in metrics],
        "effort": [m["effort"] for m in metrics],
        "difficulty": [m["difficulty"] for m in metrics],
        "volume": [m["volume"] for m in metrics],
        "length": [m["length"] for m in metrics],
        "cyclomatic_complexity": [m["cyclomatic_complexity"] for m in metrics],
        "loc": [m["loc"] for m in metrics],
    }

    export_dict = {
        "metrics": metrics,
        "stats": stats,
        "prediction": {"next_effort": next_effort},
        "chart_data": chart_data,
    }

    path = _save_to_json(
        export_dict, "export_dict.json" + datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    trend_logger.info(f"chart data saved to {path}")

    return export_dict


def markdown_fmt(result: Dict, image: str) -> str:
    """
    Args:
        result (Dict): The analysis result containing metrics, statistics, predictions, and chart data.
        image (str): The path to the image file for visualizations.

    Returns:
        str: A markdown formatted report summarizing the analysis result.

    Brief:
        Generates a markdown formatted report from the analysis result.
    """
    report = f"""
# Complexity Trend Analysis

---

### Summary

- **Files Analyzed:** {len(result['metrics'])}

---

### Statistics Overview (Model Predictions)

| Metric                | Mean     | Std Dev  |
|-----------------------|----------|----------|
| Effort                | {result['stats']['effort']['mean']:.2f}     | {result['stats']['effort']['std']:.2f}     |
| Difficulty            | {result['stats']['difficulty']['mean']:.2f} | {result['stats']['difficulty']['std']:.2f} |
| Volume                | {result['stats']['volume']['mean']:.2f}     | {result['stats']['volume']['std']:.2f}     |
| Length                | {result['stats']['length']['mean']:.2f}     | {result['stats']['length']['std']:.2f}     |
| Cyclomatic Complexity | {result['stats']['cyclomatic_complexity']['mean']:.2f} | {result['stats']['cyclomatic_complexity']['std']:.2f} |
| LOC                   | {result['stats']['loc']['mean']:.2f}        | {result['stats']['loc']['std']:.2f}        |

> _Note: These values are predicted by a trained model, not derived via traditional metrics._

---

### Prediction

- **Next File Effort:** `{result['prediction']['next_effort']:.2f}`

---

### Visualizations

![Complexity Trends]({image}) can be found in the `data/plots` directory. There is only one file in there, so you can't miss it.

---
             """

    return report


def export_to_json(result: Dict, filename: str) -> Dict:
    """_summary_

    Args:
        result (Dict): The analysis result containing metrics, statistics, predictions, and chart data.
        filename (str): The name of the file to save the chart configuration.

    Returns:
        _type_: the chart configuration dictionary
    """
    chart_config = {
        "type": "line",
        "data": {
            "labels": result["chart_data"]["labels"],
            "datasets": [
                {
                    "label": "Effort",
                    "data": result["chart_data"]["effort"],
                    "borderColor": "#FF6384",
                    "fill": False,
                },
                {
                    "label": "Difficulty",
                    "data": result["chart_data"]["difficulty"],
                    "borderColor": "#36A2EB",
                    "fill": False,
                },
                {
                    "label": "Volume",
                    "data": result["chart_data"]["volume"],
                    "borderColor": "#FFCE56",
                    "fill": False,
                },
                {
                    "label": "Length",
                    "data": result["chart_data"]["length"],
                    "borderColor": "#4BC0C0",
                    "fill": False,
                },
                {
                    "label": "Cyclomatic Complexity",
                    "data": result["chart_data"]["cyclomatic_complexity"],
                    "borderColor": "#9966FF",
                    "fill": False,
                },
                {
                    "label": "LOC",
                    "data": result["chart_data"]["loc"],
                    "borderColor": "#FF9F40",
                    "fill": False,
                },
            ],
        },
        "options": {
            "responsive": True,
            "scales": {
                "y": {
                    "beginAtZero": True,
                    "title": {"display": True, "text": "Metric Value"},
                },
                "x": {"title": {"display": True, "text": "File"}},
            },
        },
    }
    path = _save_to_json(chart_config, filename)
    trend_logger.info(f"chart data saved to {path}")

    return chart_config


def main(list_of_files: List[str]) -> Tuple:
    """_summary_

    Args:
        list_of_files (List[str]): A list of file paths to Python files to analyze.

    Raises:
        FileNotFoundError: If no Python files are provided for trend analysis.
        CodeProcessingError: If there is an error during the analysis process.

    Returns:
        Tuple(Dict, Dict): A tuple containing the chart configuration and the analysis result.
    """
    if not list_of_files:
        msg = "No Python files provided for trend analysis"
        trend_logger.error(msg)
        raise FileNotFoundError(msg)

    trend_logger.info(
        f"analyzing {len(list_of_files)} files: {[f.name for f in list_of_files]}"
    )

    result = analyze_trends(list_of_files)

    if "error" in result:
        trend_logger.error(f"Error: {result['error']}")
        raise CodeProcessingError(f"Error: {result['error']}")

    return export_to_json(result, "chart_data.json"), result
