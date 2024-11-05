document.getElementById("summarize-btn").addEventListener("click", async function () {
  if (this.disabled) return; // If the button is disabled, do nothing

  const form = document.getElementById("summarize-form");
  const formData = new FormData(form); // Create a FormData object from the form

  // Show loading spinner
  document.querySelector(".spinner").style.display = "block";
  document.getElementById("error-message").textContent = ""; // Clear any previous error messages

  try {
    const response = await fetch("/summarize", {
      method: "POST",
      body: formData,
      headers: {
        "X-Requested-With": "XMLHttpRequest", // Indicates that this is an AJAX request
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status code: ${response.status}`); // Handle HTTP errors
    } else {
      const result = await response.json(); // Parse the JSON response
      if (result.error) {
        document.getElementById("error-message").textContent = result.error; // Display any server-side errors
      } else {
        document.getElementById("output-text").value = result.summary; // Display the summary
        updateWordCount("output-text", "output-word-count"); // Update the word count for the output
      }
    }
  } catch (error) {
    console.error("Error:", error); // Log the error
    document.getElementById("error-message").textContent =
      "An error occurred. Please try again."; // Display a generic error message
  } finally {
    // Hide loading spinner
    document.querySelector(".spinner").style.display = "none";
  }
});

// Function to copy the text from the output textarea
function copyText() {
  const copyText = document.getElementById("output-text");
  copyText.select(); // Select the text
  document.execCommand("copy"); // Copy the text to the clipboard
}

// Function to clear the text in the input and output textareas
function clearText() {
  document.getElementById("output-text").value = ""; // Clear the output textarea
  document.getElementById("input-text").value = ""; // Clear the input textarea
  document.getElementById("error-message").textContent = ""; // Clear any error messages
  updateWordCount("input-text", "input-word-count"); // Update the word count for the input
  updateWordCount("output-text", "output-word-count"); // Update the word count for the output
  setSummarizeButtonState(true); // Disable the summarize button
  window.location.reload(); // Reload the page

}

// Event listener for the file upload input
document.getElementById("file-upload").addEventListener("change", function (event) {
  const file = event.target.files[0]; // Get the selected file
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const text = e.target.result; // Read the file content
      document.getElementById("input-text").value = text; // Set the content in the input textarea
      updateWordCount("input-text", "input-word-count"); // Update the word count for the input
      const wordCount = countWords(text);
      if (wordCount < 70 || wordCount >= 300) {
        document.getElementById("error-message").textContent =
          "text must be between 70 and 300 words."; // Display an error message if word count is 300 or more
        setSummarizeButtonState(true); // Disable the summarize button
      } else {
        document.getElementById("error-message").textContent = ""; // Clear any error messages
        setSummarizeButtonState(false); // Enable the summarize button
      }
    };
    reader.readAsText(file); // Read the file as text
  }
});

// Event listener for the input textarea
document.getElementById("input-text").addEventListener("input", function () {
  updateWordCount("input-text", "input-word-count"); // Update the word count as the user types
  const wordcount = countWords(this.value)
  if (wordcount < 70 || wordcount > 300) {
    document.getElementById("error-message").textContent =
      "text must be between 70 and 300 words."; // Display an error message if word count is 300 or more
    setSummarizeButtonState(true); // Disable the summarize button
  } else {
    document.getElementById("error-message").textContent = ""; // Clear any error messages
    setSummarizeButtonState(false); // Enable the summarize button
  }
});

// Function to update the word count for a specified textarea
function updateWordCount(textareaId, wordCountId) {
  const text = document.getElementById(textareaId).value; // Get the text from the textarea
  const wordCount = countWords(text); // Count the words in the text
  document.getElementById(wordCountId).textContent = `Words: ${wordCount}`; // Display the word count
}

// Function to count the words in a given text
function countWords(text) {
  return text.trim().split(/\s+/).filter(word => word.length > 0).length; // Split the text by whitespace and count the words
}

// Function to enable or disable the summarize button and set the cursor style
function setSummarizeButtonState(disable) {
  const button = document.getElementById("summarize-btn");
  button.disabled = disable; // Enable or disable the button
  button.style.cursor = disable ? "not-allowed" : "pointer"; // Set the cursor style
}

// Initial word count update
updateWordCount("input-text", "input-word-count"); // Update the word count for the input textarea
updateWordCount("output-text", "output-word-count"); // Update the word count for the output textarea
setSummarizeButtonState(true); // Disable the summarize button initially
