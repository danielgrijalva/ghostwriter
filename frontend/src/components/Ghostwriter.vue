<template>
  <div>
    <nav class="navbar navbar-dark bg-dark">      
      <a class="navbar-brand mx-auto" href="#"><h2 class="mb-1">Ghostwriter</h2></a>      
    </nav>

    <div class="row">
      <div class="col suggestions">
        <div class="list-group xxx" v-if="suggestions">
          <li class="list-group-item list-group-item-action" v-for="word in suggestions" v-on:click="buildStory(word)">
            {{ word }}
          </li>
          <li class="list-group-item p-0 customWord">
            <div class="input-group">
              <input id="customWord" type="text" class="form-control" v-on:keydown.enter="buildStory(customWord)" v-model="customWord" placeholder="Or type here">
            </div>
          </li>          
        </div>
        <div v-else class="list-group">
          <li class="list-group-item list-group-item-action">
            <vue-content-loading :height="10" :speed="1">
              <rect x="15%" y="0%" rx="3" ry="3" width="70%" height="90%" />
            </vue-content-loading>            
          </li>
          <li class="list-group-item list-group-item-action">
            <vue-content-loading :height="10" :speed="1">
              <rect x="18%" y="0%" rx="3" ry="3" width="63%" height="90%" />
            </vue-content-loading>            
          </li>          
          <li class="list-group-item list-group-item-action">
            <vue-content-loading :height="10" :speed="1">
              <rect x="18%" y="0%" rx="3" ry="3" width="50%" height="90%" />
            </vue-content-loading>            
          </li>
          <li class="list-group-item list-group-item-action">
            <vue-content-loading :height="10" :speed="1">
              <rect x="15%" y="0%" rx="3" ry="3" width="70%" height="90%" />
            </vue-content-loading>            
          </li>
          <li class="list-group-item list-group-item-action">
            <vue-content-loading :height="10" :speed="1">
              <rect x="18%" y="0%" rx="3" ry="3" width="55%" height="90%" />
            </vue-content-loading>            
          </li>
          <li class="list-group-item list-group-item-action">
            <vue-content-loading :height="10" :speed="1">
              <rect x="18%" y="0%" rx="3" ry="3" width="30%" height="90%" />
            </vue-content-loading>            
          </li>                                        
        </div>
      </div>

      <div class="col pl-0">
        <div class="list-group h-100">
          <li class="list-group-item border-0 mr-3 h-100 d-flex align-items-center justify-content-center">
            <h3 class="mb-0" v-if="story">{{ story }}</h3>
            <h3 v-else-if="suggestions" class="text-black-50 mb-0">Compose...<span class="blinking-cursor">|</span></h3>
            <vcl-code v-else :height="120" :speed="1"></vcl-code>
          </li>
         <li class="list-group-item border-top-0 border-0" v-if="story">
            <button title="Delete last word" type="button" class="btn btn-outline-dark btn-actions" v-on:click="removeWord()"><i class="fas fa-backspace"></i></button>
            <button title="Restart" type="button" class="btn btn-outline-dark btn-actions" v-on:click="reset()"><i class="fas fa-undo-alt"></i></button>
            <button title="Finish here" type="button" class="btn btn-outline-dark btn-actions" v-on:click="finishStory()"><i class="fas fa-check-double"></i></button>
             <button title="Share" type="button" class="btn btn-outline-dark btn-actions"><i class="fab fa-twitter"></i></button>
          </li>
        </div>
      </div>
    </div> 
  </div>
</template>

<script>
  import axios from "axios";
  import { VueContentLoading, VclCode }  from 'vue-content-loading';
  export default {
    name: "Ghostwriter",
    components: {
      VueContentLoading,
      VclCode,
    },
    data() {
      return {
        nextWord: '',
        customWord: '',
        story: '',
        storyTokens: [],
        suggestions: null,
        spacedPunctuation: [',', '.', '!', '?', ':', ';'],
        notSpacedPunctuation: ["'", '’', '-', '–', '—'],
      };
    },
    created: function (){
      this.getSuggestions();
    },
    methods: {
      getSuggestions() {
        axios
          .get("http://127.0.0.1:8000/ghostwriter/", {
            params: {
              story: this.storyTokens.join(' '),
            }
          })
          .then(response => (this.suggestions = response.data.suggestions));
      },
      buildStory(word){
        // assert customWord/suggestion is clean
        this.nextWord = word.trim().toLowerCase();
        
        // add clicked word to story tokens
        this.storyTokens.push(this.nextWord);

        // calculate suggestions
        this.getSuggestions();

        // more human-readable story for the user
        // e.g. capitalize first letter, trim spaces between punctuation, etc
        this.formatStory(word);

        // clear custom input
        if (this.customWord){
          this.clearInput();
        }
        
      },
      formatStory(word){
        if (this.storyTokens.length == 1){
          // always capitalize first word
          word = word[0].toUpperCase() + word.substring(1);
          this.story = word + ' ';
          
        } else if (this.story.slice(-2) == '. '){
          // capitalize word after a period
          word = word[0].toUpperCase() + word.substring(1) + ' ';
          this.story = this.story + word;

        } else if (word == 'i'){
          // capitalize "I" e.g. "I am"
          word = word.toUpperCase() + ' ';
          this.story = this.story + word;

        } else if (this.notSpacedPunctuation.includes(word)){
          // remove spaces between single quotes, hyphens and dashes
          this.story = this.story.trim() + word;

        } else if (this.spacedPunctuation.includes(word)) {
          // add a space after question marks, periods, commas, colons, semicolons
          this.story = this.story.trim() + word + ' ';

        } else {
          // add a space after every normal word
          word = word + ' ';
          this.story = this.story + word; 
          
        }
      },
      removeWord(){
        // remove last word from tokens
        this.storyTokens.pop();

        // split story into words and punctuation
        var words = this.story.split(/(,|\.|\!|\?|:|;|'|’|-|–|—)| /).filter(Boolean);

        // removed word/punctuation
        var lastWord = words.pop();

        // remove lasWord from story
        this.story = this.story.trim().replace(new RegExp(lastWord + '$'), '');

        // add a space if lastWord was some punctuation mark
        if (this.spacedPunctuation.includes(lastWord) || this.notSpacedPunctuation.includes(lastWord)){
          this.story = this.story + ' ';
        }

        // recalculate suggestions
        this.getSuggestions();
      },
      reset(){
        this.nextWord = '';
        this.story = '';
        this.storyTokens = [];
        this.getSuggestions();
      },
      finishStory(){
        this.suggestions = null;
      },
      clearInput(){
        this.customWord = null;
      }      
    }
  };
</script>