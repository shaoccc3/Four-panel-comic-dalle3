# Django Project Setup with .env Configuration

This guide will help you set up your Django project to use environment variables stored in a `.env` file, such as the `OPENAI_API_KEY`.

## Prerequisites

Ensure you have the following installed:

- Django
- `python-dotenv` package

## Step 1: Install `python-dotenv`

To load environment variables from a `.env` file, you need to install the `python-dotenv` package.

pip install python-dotenv

## Step 2: Create a .env File
In the root directory of your Django project (where manage.py is located), create a .env file.

Add your OPENAI_API_KEY (and any other environment variables) to this file:

OPENAI_API_KEY=your_openai_api_key_here
