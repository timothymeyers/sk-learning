This repository is a collection of Python scripts and Jupyter notebooks that demonstrate the use of Semantic Kernel (SK)'s recent GA version to build a multi-agent collaboration chatbot demonstration.

It will be organized into several folders, each containing a specific aspect of the project. The main components of the project are as follows:

- **backend**: This folder contains the backend code for the project, including the main application logic and any necessary libraries or dependencies.
  - **agents**: This folder contains the code for the agents used in the project. Each agent is responsible for a specific task or function within the multi-agent collaboration system.
  - **tools**: This folder contains the code for the tools used by the agents. These tools are designed to assist the agents in performing their tasks and may include APIs, libraries, or other resources.
  - **server**: This folder will contain code for an MCP Server that will expose the tools for consumption by the agents (MCP Clients).
  - **utils**: This folder contains utility functions and classes that are used throughout the project. These may include helper functions, data processing tools, or other resources that are not specific to any one component of the project.
  
  Within the **backend** folder, there should also be relevant files for the following:
- **requirements.txt**: This file lists the Python packages and dependencies required to run the backend code. It should include all necessary libraries and versions to ensure compatibility.
- **README.md**: This file provides an overview of the project, including instructions for setting up and running the backend code. It should also include any relevant information about the project structure and how to use the various components.
- **python files**: including a console app that will be able to run the agents and tools in a command-line interface. This will allow users to interact with the multi-agent collaboration system without needing a graphical user interface.

- **frontend**: This folder contains the frontend code for the project. This will be a streamlit app designed to demonstrate the capabilities of the multi-agent collaboration chatbot.

- **notebooks**: This folder contains Jupyter notebooks that demonstrate the use of the Semantic Kernel (SK) library and its recent GA version. These notebooks will provide examples of how to use SK to build multi-agent collaboration systems and will serve as a reference for users looking to implement similar functionality in their own projects.

- **docs**: This folder contains documentation for the project, including design documents, user guides, and any other relevant information. This will help users understand how to use the project and its components effectively.