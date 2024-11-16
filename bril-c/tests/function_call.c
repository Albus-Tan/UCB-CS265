#include <stdio.h>

int add_one(int p)
{
	return p + 1;
}

int add_together(int arg1, int arg2)
{
	return arg1 + arg2;
}

int add_three(int p)
{
	int three = 3;
	int added = three + p;
	return added;
}

void print_two()
{
	int two = 2;
	printf("%d\n", two);
}

int main()
{
	int arg1 = 10;
	int arg2 = 2;
	int result1 = add_one(arg1);
	printf("%d\n", result1);
	printf("%d\n", add_three(arg2));
	printf("%d\n", add_together(add_three(arg1), add_three(arg2)));
	int result2 = add_together(arg1, result1);
	print_two();
	printf("%d\n", result2);
	print_two();
}