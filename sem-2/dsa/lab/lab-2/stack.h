#ifndef STACK_H
#define STACK_H

/*
exit code -> meaning
201 -> Tried to pop an empty stack
202 -> Using top on an empty stack
*/

typedef struct StackNode {
    int val;
    struct StackNode *down;
    struct StackNode *up;
} StackNode;

typedef struct Stack {
    int size;
    StackNode *top;
} Stack;

StackNode *StackNodeInit();
Stack *StackInit();
int StackSize(Stack *s);
int StackEmpty(Stack *s);
void StackPush(Stack *s, StackNode *n);
StackNode StackPop(Stack *s);
StackNode StackTop(Stack *s);
void StackNodePrint(StackNode *n);  // Implement this function depending on the node, cannot be generalized.
void StackPrint(Stack *s);

#endif