#include <iostream>
#include <stdlib.h>
#include <time.h>
#include "Inventory.hpp"

/*
Link - > https://github.com/karan/Projects#classes
        Product Inventory Project
Create an application which manages an inventory of products.
Create a product class which has a price, id, and quantity on hand.
Then create an inventory class which keeps track of various products and can sum up the inventory value.
*/

void textGUI();

Inventory* randomInventory(int numOfProducts,int priceRange, int quantityRange)
{
    srand (time(NULL));
    Inventory *tempInv = new Inventory;

    for(int i = 1; i <= numOfProducts; ++i)
    {
        Product* temp = new Product(rand()%priceRange, i, rand() % quantityRange);
        tempInv->addProduct(*temp);
    }
    return tempInv;
}

int main()
{
    textGUI();

    /*
    Inventory* inv = randomInventory(5,100,20);
    inv->printProducts();
    std::cout << inv->sumOfInventory();
    */

    return 0;
}
