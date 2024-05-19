<div id="improve-current-language-issues">

## Improve Current Language Issues

To address current language issues, follow these steps:

1. **Locate the Corresponding File:**
   - Navigate to the `data` directory and open the `languages.json` file. Find the language key corresponding to the issue and locate the respective language file in the `data\languages` directory.

2. **Edit the Language File:**
   - Update the translation text in the identified language file with your suggested fixes.

3. **Test the Language**:
    - Verify that the language texts fit within the UI widgets. If any text is too lengthy, consider using shorter forms or displaying them across multiple lines to ensure proper display and readability.
     
4. **You're all set, just create the pull request.**

<br>

</div>

---

<br>

<div id="adding-a-new-language">

## Adding a New Language

To add a new language to the application, follow these steps:

1. **Update `languages.json`:**
   - Open the `languages.json` file located in the `data\` directory of the project (`data\languages.json`).
   - Add a new entry to the JSON object with the language name as the key and a unique language code as the value.

   Example:
   ```json
   {
     "English": "en", # English
     "中文": "zh" # Chinese
     "Española": "es"  # New entry for Spanish
   }

2.  **Create the Language File**:
    - Create a new JSON file in the data\languages directory with the name corresponding to the new language code.
   
        - For example, for Spanish, create es.json in the data\languages directory.
         
    - Add the required translations ``(check current languages files)`` in this new JSON file.
    
    Example (`es.json`):

    ```json
    {
     "video": "Video",
     "playlist": "Lista",
     "add +": "Añadir +",
     "added": "Añadido"
    }

3. **Test the Language**:
    - Verify that the language texts fit within the UI widgets. If any text is too lengthy, consider using shorter forms or displaying them across multiple lines to ensure proper display and readability.

4. **You're all set, just create the pull request**

<br>

</div>

---

**Thank you very much for your assistance with the languages in the app! Your help is greatly appreciated and will have a significant impact on our users. Excellent work!**
