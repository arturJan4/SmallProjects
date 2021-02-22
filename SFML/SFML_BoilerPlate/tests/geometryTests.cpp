#include <gtest/gtest.h>
#include <geometry.hpp>

TEST(ExampleTests, DemonstrateMacros)
{
    EXPECT_TRUE(true);
}

// deliberately failing test
TEST(ExampleTests, LibraryWorks)
{
    Tests fine;
    EXPECT_EQ("Hello", fine.Hello());

    // Arrange
    std::string actual = fine.Hello();
    // Act
    std::string expected = "Helloo";
    // Assert
    EXPECT_EQ(expected, actual);

    EXPECT_EQ("Helloo", fine.Hello());   // if Expect fails it doesn't end the test case
    ASSERT_EQ("Helloo", fine.Hello());   // if Assert fails it ends the test
    EXPECT_EQ("Helloo", fine.Hello());
}

TEST(ExampleTests, SomeDivison)
{
    Tests fine;

    EXPECT_NEAR(1.0 / 3, 0.3333, 0.1);
}