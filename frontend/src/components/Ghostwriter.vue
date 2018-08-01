<template>
  <div id="wrapper" v-bind:class="{ toggled: options }">
    <div id="page-content-wrapper">
      <div class="row  page-content-wrapper ghostwriter">        
        <div class="col-sm-1 text-left">
          <button class="btn btn-lg btn-link toggleOptions" v-on:click="toggleOptions">
            <i class="fas fa-cog"></i>
          </button>
        </div>

        <div class="col-sm-11 text-center">
          <!-- <img class="img-fluid" width="200px" src="../assets/logo.png"> -->
          <h1>Ghostwriter</h1>

          <!-- story -->
          <blockquote class="blockquote text-center">
            <p v-model="story" class="mb-0">{{ story }}</p>
            <footer v-if="story" class="blockquote-footer">{{ author }}</footer>
          </blockquote>

          <!-- suggestions -->
          <div class="suggestions-container" v-if="suggestions">
            <div class="suggestions-results" aria-labelledby="autosuggest">
              <ul role="listbox" aria-labelledby="autosuggest">
                <li v-for="word in suggestions" v-on:click="buildStory(word)" class="suggestions-results-item">
                  {{ word }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div id="sidebar-wrapper">
      <ul class="sidebar-nav">
        <li>
          <label for="topN" >Number of suggestions ({{ topNShow }})</label>
          <input type="range" v-model.lazy="topN" v-model="topNShow" v-on:change="getSuggestions" class="custom-range" min="1" max="10" value="5" step="1">          
        </li>
        <hr>
        <li>
          <label for="topN" >Change author</label>
          <input type="text" v-model="author" class="form-control mb-2" id="author" placeholder="A Recurrent Neural Network">           
        </li>
      </ul>       
    </div>
  </div>
</template>

<script>
  import axios from "axios";
  export default {
    name: "Ghostwriter",
    data() {
      return {
        options: false,
        nextWord: '',
        story: '',
        rawStory: '',
        suggestions: null,
        topN: 5,
        topNShow: 5,
        author: 'A Recurrent Neural Network'
      };
    },
    created: function (){
      var vm = this;
      this.getSuggestions();
      window.addEventListener('keydown', function(event) {
        if (event.keyCode == 8 && vm.story) { 
          vm.removeWord();
        }
      });      
    },
    methods: {
      getSuggestions() {
        axios
          .get("http://127.0.0.1:8000/ghostwriter/", {
            params: {
              topN: this.topN,
              nextWord: this.nextWord,
              story: this.rawStory
            }
          })
          .then(response => (this.suggestions = response.data.suggestions));
      },
      buildStory(word){
        if (word != '<s>'){
          this.nextWord = word;
          // raw words and characters separated by spaces,
          // used by the algorithm to do inference
          this.rawStory = (this.rawStory + ' ' + word).trim();
          this.getSuggestions();

          // more human-readable story, for user presentation
          // capitalize first letter, trim spaces between symbols, etc
          this.formatStory();
        } else {
          // user selected META_TOKEN (<end> of string).
          // META_TOKEN usually gets suggested when the story should end.
          this.suggestions = null;
        }
      },
      formatStory(){
        this.story = this.rawStory[0].toUpperCase() + this.rawStory.substring(1);
      },
      removeWord(){
        var words = this.rawStory.split(' ');
        words.pop();

        if (words.length == 0) {
          this.reset();
        } else {
          this.rawStory = words.join(' ');
          this.formatStory();
        }

        this.getSuggestions();
      },
      reset(){
        this.nextWord = '';
        this.rawStory = '';
        this.story = '';
      },
      toggleOptions(){
        this.options = !this.options;
      },
    }
  };
</script>