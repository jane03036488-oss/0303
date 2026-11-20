#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node *left;
    struct Node *right;
};

struct Node* createNode(int value) {
    struct Node *newNode = (struct Node*)malloc(sizeof(struct Node));
    if (newNode == NULL) {
        printf("記憶體配置失敗\n");
        exit(1);
    }
    newNode->data = value;
    newNode->left = NULL;
    newNode->right = NULL;
    return newNode;
}

int main() {
    struct Node *root = createNode(50);
    root->left = createNode(30);
    root->right = createNode(80);

    printf("Root: %d, Left: %d, Right: %d\n",
           root->data, root->left->data, root->right->data);

    free(root->left);
    free(root->right);
    free(root);

    return 0;
}