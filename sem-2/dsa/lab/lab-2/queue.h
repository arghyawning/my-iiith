#ifndef QUEUE_H
#define QUEUE_H

/*
exit code -> meaning
101 -> Tried to Dequeue an empty queue
102 -> Using front on an empty queue
*/

typedef struct QueueNode {
    int val;
    struct QueueNode *prev;
    struct QueueNode *next;
} QueueNode;

typedef struct Queue {
    int size;
    QueueNode *front;
    QueueNode *back;
} Queue;

QueueNode *QueueNodeInit();
Queue *QueueInit();
int QueueSize(Queue *q);
int QueueEmpty(Queue *q);
void QueueEnqueue(Queue *q, QueueNode *n);
QueueNode QueueDequeue(Queue *q);
QueueNode QueueFront(Queue *q);
void QueueNodePrint(QueueNode *n);  // Implement this function depending on the node, cannot be generalized.
void QueuePrint(Queue *q);

#endif