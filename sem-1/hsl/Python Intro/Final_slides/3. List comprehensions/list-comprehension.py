# Example for cross product of vectors represented as lists

vec = [2,4,6]
print([3*x for x in vec]) #[6, 12, 18]
print([{x: x**2} for x in vec]) #[{2: 4}, {4: 16}, {6: 36}]

#cross products:
vec1 = [2,4,6]
vec2 = [4,3,-9]
print([x*y for x in vec1 for y in vec2]) #[8,6,-18, 16,12,-36, 24,18,-54]
print([vec1[i]*vec2[i] for i in range(len(vec1))]) #[8,12,-54]

#condition
print([3*x for x in vec if x > 3]) #[12, 18]
print([3*x for x in vec if x < 2]) #]

