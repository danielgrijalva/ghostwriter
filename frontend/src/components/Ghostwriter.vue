<template>
  <div>
    <div class="row">
      <div class="col">
        <div class="ghostwriter">
          <h1>Ghostwriter</h1>

          <!-- story -->
          <blockquote class="blockquote text-center">
            <p v-model="story" class="mb-0">{{ story }}</p>
            <footer class="blockquote-footer">{{ author }}</footer>
          </blockquote>

          <!-- suggestions -->
          <div class="suggestions-container" v-if="suggestions">
            <div class="suggestions-results" aria-labelledby="autosuggest">
              <ul role="listbox" aria-labelledby="autosuggest">
                <li v-for="s in suggestions" v-on:click="buildStory(s)" class="suggestions-results-item">
                  {{ s }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-sm-3">
        <label for="topN" >Number of suggestions ({{ topNShow }})</label>
        <input type="range" v-model.lazy="topN" v-model="topNShow" v-on:change="getSuggestions" class="custom-range" min="1" max="10" value="5" step="1">
        <label for="topN" >Change author</label>
        <input type="text" v-model="author" class="form-control mb-2" id="author" placeholder="A Recurrent Neural Network">        
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
        nextWord: '',
        story: '',
        suggestions: null,
        topN: 5,
        topNShow: 5,
        author: 'A Recurrent Neural Network'
      };
    },
    created: function (){
      this.getSuggestions()
    },
    methods: {
      getSuggestions() {
        axios
          .get("http://127.0.0.1:8000/ghostwriter/", {
            params: {
              topN: this.topN,
              nextWord: this.nextWord,
              story: this.story
            }
          })
          .then(response => (this.suggestions = response.data.suggestions));
      },
      buildStory(word){
        if (word != '<end>'){
          this.nextWord = word;
          
          // raw words and characters separated by spaces,
          // used by the algorithm to do inference
          var raw = (this.story + ' ' + word).trim().trim('<end>')

          // more human-readable story, for user presentation
          // capitalize first letter, trim spaces between symbols, etc
          var edit = raw[0].toUpperCase() + raw.substring(1)
          this.story = edit

          this.getSuggestions(this.nextWord, raw)
        }else{
          // user selected META_TOKEN (<end> of string).
          // usually, META_TOKEN gets suggested when the
          // story should end.
          this.suggestions = null;
        }
      },
    }
  };
</script>

<style>
  body {
    max-width: 100%;
    padding: 20px;
    margin-left: auto !important;
    margin-right: auto !important;
  }

  .suggestions-container {
    position: relative;
    margin: auto;
    max-width: 500px;
  }
  
  .suggestions-results {
    font-weight: 300;
    margin: 0;
    position: absolute;
    z-index: 10000001;
    width: 100%;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
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

  .form-control:focus {
    border-color: #ced4da;
    box-shadow: none;
  }
</style>