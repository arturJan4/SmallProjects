#ifndef PRODUCT_HPP_INCLUDED
#define PRODUCT_HPP_INCLUDED
#include <iostream>

class Product
{
private:
    double m_price{-1};
    int m_id{-1};
    int m_quantity{-1};

public:
    Product(int id): m_id(id) {};
    Product(double price, int id, int quantity) : m_price(price), m_id(id), m_quantity(quantity)
    {
        if(price < 0 || quantity < 0)
            std::cout << "error - bad price or quantity\n";
    }

    void printProduct();

    void setQuantity(int quantity);
    void setPrice(double price);

    double getPrice();
    int getQuantity();
    int getId();
};


#endif // PRODUCT_HPP_INCLUDED
