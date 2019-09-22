#include "Inventory.hpp"

void textGUI()
{
    Inventory* tempInv{nullptr};
    Product* tempProduct{nullptr};
    double tempPrice{-1};
    int tempQuantity{-1}, tempId{-1};

    while(!0)
    {
        std::cout   << "==============================================\n";
        std::cout   << "1.Create an inventory (will override current!)\n"
                    << "2.Print an inventory                          \n"
                    << "3.Sum inventory value                         \n"
                    << "4.Add item to inventory                       \n"
                    << "5.Delete item from inventory                  \n"
                    << "6.Create an item (will override current!)     \n"
                    << "7.Show current item                           \n"
                    << "8.Quit                                        \n";

        int option{-1};
        std::cin >> option;

        system("CLS"); // optional - for WINDOWS

        if(option == 8)
            break;
        else if(option > 8 || option < 1)
        {
            std::cout << "wrong number\n";
            continue;
        }

        switch(option)
        {
        case 1:
            tempInv = new Inventory;
            break;

        case 2:
            if(tempInv != nullptr)
            {
                tempInv->printProducts();
            }
            else
                std::cout << "Error - empty inventory \n";
            break;

        case 3:
            if(tempInv != nullptr)
            {
                std::cout << "Inventory sums to : "<< tempInv->sumOfInventory() << " \n";
            }
            else
                std::cout << "Error - empty inventory \n";
            break;

        case 4:
            if(tempProduct != nullptr && tempInv != nullptr)
            {
                tempInv->addProduct(*tempProduct);
            }
            else
            {
                std::cout << "Error - item or inventory are empty\n";
            }
            break;

        case 5:
            int id;
            std::cout << "Enter id of an item you want to delete: ";
            std::cin >> id;
            tempInv->deleteProduct(id);

            break;

        case 6:
            std::cout << "enter price:    ";
            std::cin >> tempPrice;
            std::cout << "enter id:       ";
            std::cin >> tempId;
            std::cout << "enter quantity: ";
            std::cin >> tempQuantity;
            tempProduct = new Product(tempPrice,tempId,tempQuantity);

            break;

        case 7:
            if(tempProduct != nullptr)
            {
                tempProduct->printProduct();
            }
            else
            {
                std::cout << "no current item!\n";
            }
            break;

        }

    }
}
