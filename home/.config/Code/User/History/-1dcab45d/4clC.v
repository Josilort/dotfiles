fn main() {
	println(add(77, 33))
	println(sub(100, 50))

	returning_multiple_values()
	
	variables()
}

fn add(x int, y int) int {
	return x + y
}

fn sub(x int, y int) int {
	return x - y
}

fn foo() (int, int) {
		return 2, 3
	}

fn returning_multiple_values() {
	a, b := foo()
	println(a) // 2
	println(b) // 3
	c, _ := foo() // ignore values using `_`
}

pub fn public_function() {
}

fn private_function() {
}

fn variables() {
	name := 'Bob'
	age := 20
	large_number := i64(9999999999)
	println(name)
	println(age)
	println(large_number)
}

fn mutable_variables() {
	mut age := 20
	println(age)
	age = 21
	println(age)
}