# Castillo, Invoice Basic Administrator
#### Video Demo: 
#### Description:
The "Castillo" project is a web application serving as a basic invoice administrator, empowering users to efficiently manage their invoices. It enables the addition of new invoices, editing existing ones, conducting advanced searches, and more. Below is a detailed description of the project's features.

## Key Features
1. **Add Invoices:** Users can add new invoices by providing details such as amount, category, date, description, and status.
2. **Edit Invoices:** Allows the editing of existing invoices, including updates to description, amount, status, date, and category.
3. **Advanced Search:** Offers advanced search functionality, enabling users to filter invoices based on criteria like category, status, and amount range.
4. **Invoice Listing:** Provides a comprehensive view of all invoices, distinguishing between pending and paid invoices.
5. **Intuitive Interface:** Simple and user-friendly design for an optimal user experience.

## Usage
Using the system is straightforward:

1. **Add Invoices:** Fill in the required fields in the add invoice form.
2. **Edit Invoices:** Enter the invoice ID in the corresponding form for editing.
3. **Delete Invoices:** Select the delete invoice option and confirm the operation.
4. **Advanced Search:** Utilize the filters available on the search page to find specific invoices.
5. **Basic Accounting:** View financial information on the homepage.

## Project Structure

## Static Folder
This folder contains files not meant to be frequently changed, including CSS styles, the 'normalize' file, and JavaScript.

### styles.css
Styles are divided based on project sections, ranging from login and register to the index section. Root variables define the main colors of the web app.

### normalize.css
A tool ensuring consistent baseline styles in web design, addressing browser-specific variations before applying project-specific styles.

### script.js
Includes functions for form validation, success and error messaging using SweetAlert2, and asynchronous search functionality.

## Templates Directory

### layout.html
Defines the web page layout, incorporating Bootstrap for styling, Google Fonts for fonts, and custom styles from 'normalize.css' and 'styles.css.' Features a navigation bar with options based on user session status. Main content is within a 'main' tag, with additional functionality from 'script.js.' Utilizes SweetAlert2 for user-friendly alerts.

### register.html
Extends the base design, rendering the registration page. Utilizes Jinja syntax, capturing new user details and incorporating client-side validation through JavaScript. Handles potential registration errors, contributing to a robust registration process.

### login.html
Renders the login page, featuring a form for user login. Displays danger alerts for potential login errors, ensuring an accessible and visually pleasing login experience.

### add.html
Specifically designed for adding new invoices, featuring a form with fields for category, amount, date, status, and description. Utilizes various input types and displays success or danger alerts based on form submission outcomes.

### list.html
Dedicated to presenting pending and paid invoices in tables, dynamically generating content based on datasets. Enhances the user experience by providing a comprehensive view of invoices in a structured format.

### search.html
Focuses on providing a user-friendly interface for searching invoices based on specified criteria. Includes a form for inputting search parameters and dynamically displays search results.

### edit.html
Incorporates dynamic forms for searching, viewing, and editing invoices. Provides clear feedback with error and success messages, allowing seamless deletion or modification of invoices.

### index.html
Serves as the homepage, providing a basic financial overview and the ability to filter invoices based on different criteria. Incorporates interactive filters for month, year, category, and status, displaying total amounts and the number of invoices meeting specified conditions.

### helpers.py
Contributes to application security and user experience by enforcing authentication for protected routes and presenting currency amounts uniformly.

### app.py
The backbone of the Flask web application, incorporating routes and functionalities. Utilizes SQLite for database management, with routes for user authentication, invoice management, and data visualization.

### facturas.db
The database includes two primary tables: "users" and "invoices." The "users" table stores user information, and the "invoices" table records invoice details, linked by a foreign key relationship.

## Technologies Used
- Flask (Python)
- SQLite
- HTML
- CSS
- JavaScript

## Ideas and Challenges
Ideas included dynamic searching, visualizing data through graphics, and the use of hidden forms. Challenges arose during the editing process, leading to the discovery of hidden forms and ultimately providing a valuable learning experience.