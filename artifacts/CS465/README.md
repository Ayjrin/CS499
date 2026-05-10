# CS465
---

## Architecture

### Frontend Development Types
In this full-stack project, there are two approaches to frontend development used:

**Express HTML (Server-Side Rendering):**
For the customer-facing side of the application, app_server, I used Express with Handlebars templates. In this model, the server constructs the complete HTML document before sending it to the client. This approach is good for static content, SEO, and ensuring the site is viewable even on devices with limited JavaScript capabilities. The browser receives a fully rendered page, reducing the initial processing load on the client.

**Single-Page Application (SPA) with Angular:**
For the administrative interface, app_admin, I built a Single Page Application using the Angular framework. Unlike the server-side rendering, the SPA loads a single HTML shell once. Subsequent interactions use JavaScript to dynamically rewrite the current page with new data fetched from the API, rather than loading entire new pages from the server. This gives the user a smoother user experience with faster transitions and reduced bandwidth usage, as only json data is transmitted after the initial load.

### NoSQL MongoDB Backend
The backend uses MongoDB, a NoSQL database, for its flexibility and seamless integration with the JavaScript ecosystem. MongoDB stores data in BSON format, which maps to the JavaScript objects used in both the Express backend and Angular frontend. This gets rid of the need for complex Object-Relational Mapping (ORM) layers often required with SQL databases and allows for faster development cycles and easier handling of unstructured or partially structured data like travel itinerary details.

---

## Functionality

### JSON vs. JavaScript
**JavaScript** is the programming language used to write the logic for the application, both on the server and in the browser. It defines functions, variables, and behavior.

**JSON (JavaScript Object Notation)** is a text-based data format. While it has similar JavaScript object syntax, it is not dependent on JS as a language.

In this project, JSON acts as the format for the data sent between the frontend and backend. When the Angular frontend requests trip data, the Express API retrieves BSON data from MongoDB, converts it to JavaScript objects, and then serializes it into a JSON string to send over the network. The frontend parses this JSON back into JavaScript objects to display to the user.

### Refactoring and Reusable UI
One instance of refactoring involved moving from hardcoded data access to a RESTful API architecture. Initially, the application might simply render views with static data or direct database calls within the route handler. I refactored this by creating a dedicated API layer that serves data via HTTP endpoints. This allowed the Angular frontend to consume the same data source as the customer facing site. Using a framework like Angular gives uis the ability to create reusable components, such as the TripCardComponent. Instead of duplicating the HTML and CSS for every trip displayed on the dashboard, I created a single component that accepts a trip object as an input. This encapsulates the logic and styling in one place. If I need to update the design of the trip card, I only have to do it once, and the change propagates everywhere the component is used. This dramatically helps maintainability and code readability.

---

## Testing

### Methods, Endpoints, and Security
*   **Methods:** I utilized standard HTTP verbs like GET (retrieving trips), POST (adding a trip), PUT (updating a trip), and DELETE (removing a trip) to perform CRUD operations. I tested the backend using Postman and then did ad hoc end to end tests to test the whole system as a user.
*   **Endpoints:** These methods target specific endpoints (e.g., /api/trips or /api/trips/:code).
*   **Security:** Testing became more complex with the addition of security layers. I implemented JWT (JSON Web Token) authentication to secure the admin routes. Testing involved ensuring that public endpoints, like viewing trips, remained accessible, while protected endpoints, like adding or editing trips, correctly rejected requests without a valid token. This required configuring the test environment to mock authenticated states and verify that unauthorized users were blocked, making sure the integrity and security of the application data.

---

## Reflection

### Professional Goals and Marketable Skills
This course has been helpful in exposing me to Angular. In my job as a full stack web dev, I use React day to day and have not had the time to try other solutions. I find Angular's opinionated approach interesting, but I won't be dropping React anytime soon. This exposure has made me want to try other solutions however such as Svelte.
