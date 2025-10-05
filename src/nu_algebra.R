NU_add <- function(x, y) {
  c(n = x[1] + y[1], u = x[2] + y[2])
}
NU_mul <- function(x, y) {
  c(n = x[1] * y[1], u = x[1] * y[2] + y[1] * x[2])
}
NU_scalar <- function(a, x) {
  c(n = a * x[1], u = abs(a) * x[2])
}
# Example usage:
x <- c(10, 1)   # (n, u)
y <- c(5, 0.5)
cat("x + y =", NU_add(x, y), "\n")
cat("x * y =", NU_mul(x, y), "\n")
cat("2 * x =", NU_scalar(2, x), "\n")
