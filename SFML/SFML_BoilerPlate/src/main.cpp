#include <SFML/Graphics.hpp>
#include <geometry.hpp>

int main()
{
    // just basic window rendering from SFML tutorial
    sf::RenderWindow window(sf::VideoMode(800, 800), "Game 1", sf::Style::Titlebar | sf::Style::Close);
    sf::CircleShape shape(100.f);
    shape.setFillColor(sf::Color::Green);

    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear();
        window.draw(shape);
        window.display();
    }

    return 0;
}