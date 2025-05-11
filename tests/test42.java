// name: check_compatibility
// label: 42
// method_tested: is_valid_file()
// should_fail: False
public class test42 {
  public static void main(String[] args) {
      String input = "Hello, world!";
      String reversed = new StringBuilder(input).reverse().toString();
      System.out.println("Original: " + input);
      System.out.println("Reversed: " + reversed);
  }
}