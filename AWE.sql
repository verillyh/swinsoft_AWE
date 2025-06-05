DROP TABLE IF EXISTS Order_Item;
DROP TABLE IF EXISTS Invoice;
DROP TABLE IF EXISTS Order_Record;
DROP TABLE IF EXISTS Product_Good;
DROP TABLE IF EXISTS Brand_Category;
DROP TABLE IF EXISTS Brand;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Inbox_Message;
DROP TABLE IF EXISTS Account;

CREATE TABLE Account (
    AccountID       INT             AUTO_INCREMENT  PRIMARY KEY,
    Email           VARCHAR(100)    NOT NULL        UNIQUE,
    UserName        VARCHAR(100)    NOT NULL,
    Password        VARCHAR(100)    NOT NULL,
    StreetAddress   VARCHAR(100)    NOT NULL,
    AccountType     ENUM('OWNER', 'STAFF', 'CUSTOMER') NOT NULL
);

CREATE TABLE Order_Record (
    OrderID         INT             AUTO_INCREMENT  PRIMARY KEY,
    CustomerID      INT             NOT NULL,
    OrderDate       DATETIME        NOT NULL,
    OrderStatus     ENUM('PENDING', 'PAID', 'SHIPPED', 'CANCELLED') NOT NULL,
    TotalPrice      DECIMAL(10,2)   NOT NULL,
    CustomerName    VARCHAR(100)    NOT NULL,
    PhoneNumber     VARCHAR(100)    NOT NULL,
    ShippingAddress VARCHAR(100)    NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Account(AccountID)
);

CREATE TABLE Invoice (
    InvoiceID       INT             AUTO_INCREMENT  PRIMARY KEY,
    OrderID         INT             NOT NULL,
    CustomerID      INT             NOT NULL,
    AmountDue       DECIMAL(10,2)   NOT NULL,
    InvoiceStatus   ENUM('PENDING', 'PAID', 'CANCELLED') NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Order_Record(OrderID),
    FOREIGN KEY (CustomerID) REFERENCES Account(AccountID)
);

CREATE TABLE Category (
    CategoryID      INT             AUTO_INCREMENT  PRIMARY KEY,
    CategoryName    VARCHAR(100)    NOT NULL        UNIQUE
);

INSERT INTO Category (CategoryName)
VALUES
  ('TELEVISION'),
  ('MOBILEPHONE'),
  ('COMPUTER_LAPTOP');

CREATE TABLE Brand (
    BrandID         INT             AUTO_INCREMENT  PRIMARY KEY,
    BrandName       VARCHAR(100)    NOT NULL        UNIQUE
);

INSERT INTO Brand (BrandName)
VALUES
  ('SAMSUNG'),
  ('LG'),
  ('SONY'),
  ('PANASONIC'),
  ('TCL'),
  ('APPLE'),
  ('GOOGLE'),
  ('ONEPLUS'),
  ('XIAOMI'),
  ('MOTOROLA'),
  ('DELL'),
  ('HP'),
  ('LENOVO'),
  ('ASUS'),
  ('ACER');

CREATE TABLE Brand_Category (
    BrandID         INT             NOT NULL,
    CategoryID      INT             NOT NULL,
    PRIMARY KEY (BrandID, CategoryID),
    FOREIGN KEY (BrandID)    REFERENCES Brand(BrandID)    ON DELETE CASCADE,
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID) ON DELETE CASCADE
);

INSERT INTO Brand_Category (BrandID, CategoryID)
VALUES
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'SAMSUNG'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'TELEVISION')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'SAMSUNG'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'MOBILEPHONE')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'SAMSUNG'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'COMPUTER_LAPTOP')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'LG'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'TELEVISION')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'LG'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'COMPUTER_LAPTOP')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'SONY'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'TELEVISION')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'SONY'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'COMPUTER_LAPTOP')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'PANASONIC'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'TELEVISION')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'TCL'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'TELEVISION')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'APPLE'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'MOBILEPHONE')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'APPLE'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'COMPUTER_LAPTOP')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'GOOGLE'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'MOBILEPHONE')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'ONEPLUS'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'MOBILEPHONE')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'XIAOMI'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'MOBILEPHONE')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'MOTOROLA'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'MOBILEPHONE')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'DELL'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'COMPUTER_LAPTOP')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'HP'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'COMPUTER_LAPTOP')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'LENOVO'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'COMPUTER_LAPTOP')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'ASUS'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'COMPUTER_LAPTOP')
  ),
  (
    (SELECT BrandID FROM Brand WHERE BrandName = 'ACER'),
    (SELECT CategoryID FROM Category WHERE CategoryName = 'COMPUTER_LAPTOP')
  );

CREATE TABLE Product_Good (
    ProductID       INT             AUTO_INCREMENT  PRIMARY KEY,
    Name            VARCHAR(100)    NOT NULL,
    Description     VARCHAR(100)    NOT NULL,
    UnitPrice       DECIMAL(10,2)   NOT NULL,
    StockQuantity   INT             NOT NULL,
    CategoryID      INT             NOT NULL,
    BrandID         INT             NOT NULL,
    IsActive 		TINYINT(1) 		NOT NULL 		DEFAULT 1,
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID),
    FOREIGN KEY (BrandID)    REFERENCES Brand(BrandID),
    FOREIGN KEY (BrandID, CategoryID)
        REFERENCES Brand_Category(BrandID, CategoryID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE Order_Item (
    OrderItemID     INT             AUTO_INCREMENT  PRIMARY KEY,
    OrderID         INT             NOT NULL,
    ProductID       INT             NOT NULL,
    Quantity        INT             NOT NULL,
    UnitPrice       DECIMAL(10,2)   NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Order_Record(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Product_Good(ProductID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE Inbox_Message (
  MessageID         INT             AUTO_INCREMENT  PRIMARY KEY,
  RecipientID       INT             NOT NULL,
  Sender            VARCHAR(255)    NOT NULL,
  Content           TEXT            NOT NULL,
  IsRead            BOOLEAN         NOT NULL        DEFAULT FALSE,
  CreatedAt         DATETIME        NOT NULL        DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (RecipientID) REFERENCES account(AccountID)
);
