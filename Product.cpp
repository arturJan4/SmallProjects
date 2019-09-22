#include "Product.hpp"

void Product::printProduct()
{
    std::cout << "Product ID: "  << m_id << "\n"
              << "Price     : "  << m_price << "\n"
              << "Quantity  : "  << m_quantity << "\n";

}

void Product::setQuantity(int quantity)
{
    if(quantity >= 0)
    {
        m_quantity = quantity;
    }
    else
        std::cout << "error - bad quantity\n";
}

void Product::setPrice(double price)
{
    if(price >= 0)
    {
        m_price = price;
    }
    else
        std::cout << "error - bad price\n";
}

double Product::getPrice()
{
    return m_price;
}

int Product::getQuantity()
{
    return m_quantity;
}

int Product::getId()
{
    return m_id;
}
