#include "Inventory.hpp"

void Inventory::addProduct(Product product)
{
    int id = product.getId();
    bool found = false; //check for duplicate ID's
    for(auto i : m_products)
    {
        if(i.getId() == id)
        {
            found = true;
            break;
        }
    }
    if(found)
        std::cout << "error, duplicate ID\n";
    else
        m_products.push_back(product);
}

//delete Product by giving ID
void Inventory::deleteProduct(int id)
{
    int x{0};
    for(auto i : m_products)
    {
        if(i.getId() == id)
        {
            m_products.erase(m_products.begin() + x);
        }
        ++x;
    }
}

void Inventory::printProducts()
{
    for(auto i : m_products)
    {
        i.printProduct();
        std::cout << "\n";
    }
}

double Inventory::sumOfInventory()
{
    double sum{0};
    for(auto i : m_products)
    {
        sum += (i.getPrice()* i.getQuantity());
    }
    return sum;
}
