# Code a static website generator, static website server, and a static website with the following rules:

## Static Website Server

- Use node.js and keep the static website server simple by using the node module "serve"
- The static website server should be invoked by "npm run serve"

## Static Website Generator

- Use node.js. Do NOT use any JavaScript frameworks such as React, next.js, Angular, Express.js, or Svelte.
- Templates should use handlebars. Templates are stored in the "templates" directory.
- The static generator should use plain JavaScript and node modules and be invoked by "npm run build"
- There should be a separate template for the homepage and subpages.
Content files should be stored in the "content" directory. They should use markdown and specify the URL, title, and common meta properties for the generator to leverage.
- Use "marked" node module for handling markdown.
- Adding new markdown content files results in new statically generated HTML files.
- The website navigation should be automatically determined based on the markdown metadata in the content directory.
- The generated static website should be served from "public" directory.
- Write and run unit tests using jest to ensure the geneartor works
- Build the static website but do not serve it yet

## Repository

- Create a git repository and commit
- Exclude node modules directory from repo
