#ifndef INVENTORY_HPP_INCLUDED
#define INVENTORY_HPP_INCLUDED
#include <vector>
#include "Product.hpp"

class Inventory
{
private:
    std::vector<Product> m_products;
public:
    Inventory() {};
    Inventory(std::vector<Product> products) : m_products(products) {};

    void addProduct(Product product);
    void deleteProduct(int id); //delete Product by giving ID
    void printProducts();
    double sumOfInventory();
};

#endif // INVENTORY_HPP_INCLUDED
