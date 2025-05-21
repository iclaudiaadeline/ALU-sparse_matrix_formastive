import os
#getting list of tuples and rows and columns from file 
def getTuples(location):

    #checking if path location is valid
    if not os.path.exists(location):
        raise ValueError("invalid file location")
    
    #reading from input file
    with open(location, 'r') as file:
        try:
            #getting rows and columns 
            rows = int(file.readline().strip().split("=")[1])+1
            cols = int(file.readline().strip().split("=")[1])+1
        except:
            raise ValueError("Input file has wrong format")
        
        #extracting tuples from the file
        tuples = []
        for line in file:
            if line.startswith("(") and line.endswith(")\n"):
                values = line.strip("()\n").split(",")
                if len(values) != 3:
                    raise ValueError("Input file has wrong format")
                tuples.append(tuple(map(int, values)))
            else:
                raise ValueError("Input file has wrong format")
        #returning rows , columns and list of tuples as tuple
        return rows, cols, tuples

#defining function that creates and return zero matrix  
def Zeromatrix(r,c):
    matrix=[]
    for i in range(r):
        row=[]
        for j in range(c):
            row.append(0)
        matrix.append(row)
    return matrix

#defining function that fills zero matrix with tuples to return sparce matrix
def Sparcematrix(tuples,rows,cols):
    #creating zero matrix using defined function
    matrix=Zeromatrix(rows,cols)

    #filling tuple's value to their location in matrix
    for tuple in tuples:
        r,c,v=tuple
        if r<rows and c<cols:
         matrix[r][c]=v
        else:
            raise ValueError(f"tuple {tuple} is out of range of rows={rows} columns={cols}")
    return matrix

#difining function that returns rows and columns of matrix as tuple
def getRowsandColumns(Matrix):
    r=len(Matrix)
    c=len(Matrix[0])
    return r,c

#defining function that Adds two matrix
def Add(A,B):
    #getting rows and columns of those matrice using defined function
    i,j=getRowsandColumns(A)
    m,n=getRowsandColumns(B)

    #checking if matrice can be added
    if i==m and j==n:
        #Adding two matrice and returning sum matrix
        Sum=[]
        for r in range(i):
            row=[]
            for c in range(j):
                row.append(A[r][c]+B[r][c])
            Sum.append(row)
        return Sum
    else:
        raise ValueError("can't Add thosse matrix, number of rows and columns of 1st matrix must be equal to that of 2nd matrix")

#defining function that subutracts two matrix    
def Sub(A,B):
    #getting rows and columns of those matrice using defined function
    i,j=getRowsandColumns(A)
    m,n=getRowsandColumns(B)

    #checking if matrice can be subtracted
    if i==m and j==n:
        #Subtracting two matrice and returning result matrix
        sub=[]
        for r in range(i):
            row=[]
            for c in range(j):
                row.append(A[r][c]-B[r][c])
            sub.append(row)
        return sub
    else:
        raise ValueError("can't subtact thosse matrix, number of rows and columns of 1st matrix must be equal to that of 2nd matrix")

#defining mulitplication function    
def Multi(A,B):
    #getting rows and columns of both matrice using defined function
    i,j=getRowsandColumns(A)
    m,n=getRowsandColumns(B)

    #checking if Matrice can be multiplied
    if j==m:
        #multipliying two matrice and return result matrix
        Result=[]
        for r in range(i):
            row=[]
            for c in range(n):
                sum=0
                for k in range(j):
                    sum+=A[r][k]*B[k][c]
                row.append(sum)
            Result.append(row)
        return Result
    else:
        raise ValueError("matrice can't be multiplied, rows of first matrix must be equal to columns of second matrix")

#converting sparce matrix into tuples
def toTuples(A):
    #getting rows and columns of matrix
    rows,cols=getRowsandColumns(A)
    
    #extracting tuples from matrix and storing them in a list
    tuples=[]
    for i,row in enumerate(A):
        for j,value in enumerate(row):
            if value != 0:
                tuples.append((i,j,value))
    #returning rows,cols and list of tuples as a tuple
    return rows,cols,tuples

#writing matrix in an output file represented in list of tuples
def toFile(A,location):
    #getting rows,colums,and list of tuples using defined function
    r,c,tuples=toTuples(A)

    #populating number of rows and colums and list of tuples in output file location
    with open(location,'w') as file: #it will create the file if it doesn't exit
        file.write(f"rows = {r-1}\n")
        file.write(f"columns = {c-1}\n")
        for tuple in tuples:
            file.write(f"{tuple}\n") 

# defining main function
def main():
    #locating main directories using os module path method
    base_dir=os.path.dirname(__file__)
    input_loc=os.path.join(base_dir,"../../sample_inputs")
    output_loc=os.path.join(base_dir,"../../sample_outputs")

    # locating files input files for matrice
    matrix1_loc=os.path.join(base_dir,f"{input_loc}/matrix1.txt")
    matrix2_loc=os.path.join(base_dir,f"{input_loc}/matrix2.txt")

    # extracting rows,columns and list of tuples from allocated files
    i,j,A=getTuples(matrix1_loc)
    m,n,B=getTuples(matrix2_loc)

    #loading sparce matrix from extracted tuples
    M1=Sparcematrix(A,i,j)
    M2=Sparcematrix(B,m,n)

    #calculating sum and storing result in output file
    if i==m and j==n:
        summation=Add(M1,M2)
        toFile(summation,f"{output_loc}/summation.txt")

        #calculating Subtraction and storing result in output file
        subtraction=Sub(M1,M2)
        toFile(subtraction,f"{output_loc}/subtraction.txt")
    else:
        print("failed to calculate Sum and subtraction, number of rows and columns must be equal")
    
    #calculating Product and storing result in output file
    if j==m:
        Multiplication=Multi(M1,M2)
        toFile(Multiplication,f"{output_loc}/Multiplication.txt")
    else:
        print("failed to calculate product, columns of 1st matrix must be eqaul to rows of second matrix")

if __name__== '__main__':
    main()