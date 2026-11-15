#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

/* Do not change the function signatures. Write the whole program below. */
void printMenu();
int getMenu();
void printMatrix(int matrix[][50], int rows, int cols);
void initMatrix(int matrix[][50], int rows, int cols);
void transposeMatrix(int matrix[][50], int oldRows, int oldCols);
void sortByRows(int matrix[][50], int rows, int cols);
void sortMatrix(int matrix[][50], int rows, int cols);
int matrixValue(int matrix[][50], int rows, int cols);
void powMatrix(int matrix[][50], int size, int matPower);
int subMatrixCount(int matrix[][50], int rows, int cols, int sum);
int getValidInt(int min_val, int max_val);
void switchRows(int matrix[][50], int r1, int r2, int cols);
int sumOfRow(int matrix[][50], int cols, int r);
void multiplyMatrix(int m1[][50], int m2[][50], int size);

void main()
{
    int rows = -2147483647;
    int cols = -2147483647;
    // get rows
    while (rows == -2147483647)
    {
        printf("Insert number of rows (1-50): ");
        rows = getValidInt(1, 50);
        if (rows == -2147483647)
        {
            printf("Wrong input, try again\n");
        }
    }
    // get cols
    while (cols == -2147483647)
    {
        printf("Insert number of columns (1-50): ");
        cols = getValidInt(1, 50);
        if (cols == -2147483647)
        {
            printf("Wrong input, try again\n");
        }
    }
    // create the matrix of zeros
    int matrix[50][50] = {0};

    // menu loop
    int input = getMenu();
    while (input != 0)
    {
        int pow = -2147483647;
        int targetSum = -2147483647;
        int tmp;
        switch (input)
        {
        case 1:
            printMatrix(matrix, rows, cols);
            break;
        case 2:
            initMatrix(matrix, rows, cols);
            break;
        case 3:
            transposeMatrix(matrix, rows, cols);
            tmp = rows;
            rows = cols;
            cols = tmp;
            break;
        case 4:
            sortByRows(matrix, rows, cols);
            break;
        case 5:
            sortMatrix(matrix, rows, cols);
            break;
        case 6:
            printf("%d\n", matrixValue(matrix, rows, cols));
            break;
        case 7:
            if (rows != cols)
            {
                printf("This is not a square matrix.\n");
                break;
            }
            while (pow == -2147483647)
            {
                printf("Insert i: ");
                pow = getValidInt(1, 2147483647);
                if (pow == -2147483647)
                {
                    printf("Wrong input, try again\n");
                }
            }
            powMatrix(matrix, rows, pow);
            break;

        case 8:
            while (targetSum == -2147483647)
            {
                printf("Enter your desired sum: ");
                targetSum = getValidInt(-2147483647, 2147483647);
                if (targetSum == -2147483647)
                {
                    printf("Wrong input, try again\n");
                }
            }
            int result = subMatrixCount(matrix, rows, cols, targetSum);
            printf("%d\n", result);
            break;
        }
        input = getMenu();
    }
}

/*find count of equal sums of submats*/
int subMatrixCount(int matrix[][50], int rows, int cols, int sum)
{
    int count = 0;
    for (int r1 = 0; r1 < rows; r1++)
    {
        for (int r2 = r1; r2 < rows; r2++)
        {
            for (int c1 = 0; c1 < cols; c1++)
            {
                int current_sum = 0;
                for (int c2 = c1; c2 < cols; c2++)
                {
                    for (int i = r1; i <= r2; i++)
                    {
                        current_sum += matrix[i][c2];
                    }
                    if (current_sum == sum)
                    {
                        count++;
                    }
                }
            }
        }
    }
    return count;
}

/*pow the mat n times*/
void powMatrix(int matrix[][50], int size, int matPower)
{
    // create a copy
    int copy[50][50];
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            copy[i][j] = matrix[i][j];
        }
    }
    for (int i = 0; i < matPower - 1; i++)
    {
        multiplyMatrix(matrix, copy, size);
    }
}

/*mul 2 mats into m1*/
void multiplyMatrix(int m1[][50], int m2[][50], int size)
{
    int result[50][50];
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            result[i][j] = 0;

            for (int k = 0; k < size; k++)
            {
                result[i][j] += m1[i][k] * m2[k][j];
            }
        }
    }
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            m1[i][j] = result[i][j];
        }
    }
}

/* return the calc of sums of r*c*val*/
int matrixValue(int matrix[][50], int rows, int cols)
{
    int sum = 0;
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            sum += ((i + 1) * (j + 1) * matrix[i][j]);
        }
    }
    return sum;
}

/*sort every cell in the matrix*/
void sortMatrix(int matrix[][50], int rows, int cols)
{
    int total = rows * cols;

    for (int i = 0; i < total - 1; i++)
    {
        for (int j = 0; j < total - 1 - i; j++)
        {
            // calc the row and col of the next cell
            int r1 = j / cols;
            int c1 = j % cols;

            int r2 = (j + 1) / cols;
            int c2 = (j + 1) % cols;

            // switch if neccessary
            if (matrix[r1][c1] > matrix[r2][c2])
            {
                int tmp = matrix[r1][c1];
                matrix[r1][c1] = matrix[r2][c2];
                matrix[r2][c2] = tmp;
            }
        }
    }
}

/* return the sum of a row */
int sumOfRow(int matrix[][50], int cols, int r)
{
    int sum = 0;
    for (int i = 0; i < cols; i++)
    {
        sum += matrix[r][i];
    }
    return sum;
}

/* switch between 2 rows */
void switchRows(int matrix[][50], int r1, int r2, int cols)
{
    for (int i = 0; i < cols; i++)
    {
        int tmp = matrix[r1][i];
        matrix[r1][i] = matrix[r2][i];
        matrix[r2][i] = tmp;
    }
}

/* sort the rows by sum using bubble sort */
void sortByRows(int matrix[][50], int rows, int cols)
{
    for (int i = 0; i < rows - 1; i++)
    {
        for (int j = 0; j < rows - 1 - i; j++)
        {
            if (sumOfRow(matrix, cols, j) > sumOfRow(matrix, cols, j + 1))
            {
                switchRows(matrix, j, j + 1, cols);
            }
        }
    }
}

/*change the values of the mat*/
void initMatrix(int matrix[][50], int rows, int cols)
{
    int ch = 0;

    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            int num = 0;
            int sign = 1;
            while ((ch = getchar()) == ' ' || ch == '\t' || ch == '\n' || ch == '\r')
                ;
            if (ch == '-')
            {
                sign = -1;
                ch = getchar();
            }
            else if (ch == '+')
            {
                ch = getchar();
            }

            while (ch >= '0' && ch <= '9')
            {
                num = num * 10 + (ch - '0');
                ch = getchar();
            }

            matrix[i][j] = num * sign;
        }
    }

    while (ch != '\n' && ch != EOF)
    {
        ch = getchar();
    }
}

/*transpose the matrix*/
void transposeMatrix(int matrix[][50], int oldRows, int oldCols)
{
    int max = 0;
    if (oldRows > oldCols)
    {
        max = oldRows;
    }
    else
    {
        max = oldCols;
    }
    for (int i = 0; i < max; i++)
    {
        for (int j = i; j < max; j++)
        {
            int tmp = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = tmp;
        }
    }
}

/* show the menu and get input until ok input*/
int getMenu()
{
    int choice = -2147483647;
    while (choice == -2147483647)
    {
        printMenu();
        choice = getValidInt(0, 8);
        if (choice == -2147483647)
        {
            printf("Wrong input, try again\n");
        }
    }

    return choice;
}

/*print the main menu*/
void printMenu()
{
    printf("1. Display the matrix.\n2. Insert values to the matrix.\n3. Transpose matrix.\n4. Sort the matrix by rows sum.\n5. Sort the whole matrix.\n6. Print matrix value.\n7. i-th power of matrix.\n8. Find sub matrix.\n0. Exit.\nPlease enter your choice: ");
}

/*print the matrix*/
void printMatrix(int matrix[][50], int rows, int cols)
{
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            printf("%d", matrix[i][j]);
            if (j < cols - 1)
            {
                printf(" ");
            }
        }
        printf("\n");
    }
}

/*return -2147483647 for error else return the number input
 * analyze positive and negetive numbers */
int getValidInt(int min_val, int max_val)
{
    int ch;
    int num = 0;
    int has_digits = 0;
    int finished = 0;
    int valid = 1;
    int sign = 1;
    int has_sign = 0;
    while ((ch = getchar()) != '\n' && ch != EOF)
    {
        if (ch == ' ' || ch == '\t' || ch == '\r')
        {
            if (has_digits || has_sign)
            {
                finished = 1;
            }
        }
        else if ((ch == '-' || ch == '+') && !has_digits && !finished && !has_sign)
        {
            has_sign = 1;
            if (ch == '-')
            {
                sign = -1;
            }
        }
        else if (ch >= '0' && ch <= '9')
        {
            if (finished)
            {
                valid = 0;
            }
            else
            {
                has_digits = 1;
                num = num * 10 + (ch - '0');
            }
        }
        else
        {
            valid = 0;
        }
    }
    num = num * sign;
    if (!valid || !has_digits || num < min_val || num > max_val)
    {
        return -2147483647;
    }
    return num;
}
