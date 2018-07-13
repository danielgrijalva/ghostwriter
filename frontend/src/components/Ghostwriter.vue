<template>
  <div class="ghostwriter">
    <h1>Ghostwriter</h1>
     <div class="form-group">
      <textarea class="form-control" id="story" rows="3" v-model="story" @input="getSuggestions"></textarea>
      <div class="suggestions-container" v-if="suggestions">
        <div class="suggestions-results" aria-labelledby="autosuggest">
          <ul role="listbox" aria-labelledby="autosuggest">
            <li v-for="s in suggestions" class="suggestions-results-item">
              {{ s }}
            </li>
          </ul>
        </div>
      </div>  
    </div> 
  </div>
</template>

<script>
  import axios from "axios";
  export default {
    name: "Ghostwriter",
    data() {
      return {
        story: null,
        suggestions: null,
      };
    },
    methods: {
      getSuggestions() {
        let words = this.story.split(' ')
        axios
          .get("http://127.0.0.1:8000/ghostwriter/", {
            params: {
              text: words[words.length-1]
            }
          })
          .then(response => (this.suggestions = response.data.result));
      }
    }
  };
</script>

<style>
  textarea {
    resize: none;
    box-shadow: none !important;
  }

  body {
    max-width: 800px;
    padding: 20px;
    margin-left: auto !important;
    margin-right: auto !important;
  }

  .suggestions-container {
    position: relative;
    width: 100%;
  }
  
  .suggestions-results {
    font-weight: 300;
    margin: 0;
    position: absolute;
    z-index: 10000001;
    width: 100%;
    border: 1px solid #e0e0e0;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    background: white;
    padding: 0px;
  }
  
  .suggestions-results ul {
    list-style: none;
    padding-left: 0;
    margin: 0;
  }
  
  .suggestions-results .suggestions-results-item {
    cursor: pointer;
    padding: 15px;
  }
  
  .suggestions-results .suggestions-results-item:active,
  .suggestions-results .suggestions-results-item:hover,
  .suggestions-results .suggestions-results-item:focus {
    background-color: #ddd;
  }
</style>