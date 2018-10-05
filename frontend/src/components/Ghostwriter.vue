<template>
  <div>
    <div class="row ml-auto mr-auto">
      <div class="col">
        <h1 class="p-5 mb-0">Ghostwriter</h1>
      </div>
    </div>

    <div class="row ml-auto mr-auto" v-if="!suggestions">
      <div class="col ml-5 pl-5">
        <vcl-list :height="160" :speed="1"></vcl-list>
      </div>
    </div>  

    <div class="row ml-auto mr-auto">
      <div class="col">
        <transition name="fade">
          <h4 class="font-weight-light text-black-50 pb-5 pr-5 pl-5 mb-0" v-if="story">
            {{ story }}<span class="blinking-cursor blinking-cursor-nosp">|</span>
          </h4>
          <h4 v-else-if="suggestions" class="font-weight-light text-gray-50 pb-5 pr-5 pl-5 mb-0">
            Start writing...<span class="blinking-cursor">|</span>
          </h4>
        </transition>
      </div>
    </div>  

    <div class="row">
      <div class="col d-flex justify-content-center">
        <transition name="fade">
          <div class="list-group align-middle suggestions" v-if="suggestions">
            <li class="list-group-item list-group-item-action d-flex justify-content-between align-items-center" v-for="(word, index) of suggestions"
              v-on:click="buildStory(word)">
              {{ word }} <span class="badge badge-secondary badge-pill">{{ probs[index] }}</span>
            </li>
            <li class="list-group-item p-0 customWord">
              <div class="input-group">
                <input id="customWord" type="text" class="form-control" v-on:keydown.enter="buildStory(customWord)" v-model="customWord"
                  placeholder="Or type here...">
              </div>
            </li>
          </div>
        </transition>
      </div>
    </div>

    <transition name="fade">
      <div class="row p-5" v-if="story">
        <div class="col  d-flex justify-content-center">
            <div class="btn-group" role="group">
              <button type="button" class="btn p-2 btn-outline-secondary btn-actions" v-on:click="removeWord()">
                <i class="fas fa-backspace"></i>
              </button>
              <button type="button" class="btn p-2 btn-outline-secondary btn-actions" v-on:click="reset()">
                <i class="fas fa-redo"></i>
              </button>
              <button type="button" class="btn p-2 btn-outline-secondary btn-actions" v-on:click="finishStory()">
                <i class="fas fa-check-double"></i>
              </button>
            </div>
        </div>
      </div>      
    </transition>
  </div>
</template>

<script>
import axios from "axios";
import { VclList } from "vue-content-loading";
export default {
  name: "Ghostwriter",
  components: {
    VclList,
  },
  data() {
    return {
      nextWord: "",
      customWord: "",
      story: "",
      storyTokens: [],
      suggestions: null,
      probs: null,
      spacedPunctuation: [",", ".", "!", "?", ":", ";"],
      notSpacedPunctuation: ["'", "’", "-", "–", "—"]
    };
  },
  created: function() {
    this.getSuggestions();
  },
  methods: {
    getSuggestions() {
      axios
        .get("http://127.0.0.1:8000/ghostwriter/", {
          params: {
            story: this.storyTokens.join(" ")
          }
        })
        .then(
          response => (
            (this.suggestions = response.data.suggestions),
            (this.probs = response.data.probs)
          )
        );
    },
    buildStory(word) {
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
      if (this.customWord) {
        this.clearInput();
      }
    },
    formatStory(word) {
      if (this.storyTokens.length == 1) {
        // always capitalize first word
        word = word[0].toUpperCase() + word.substring(1);
        this.story = word + " ";
      } else if (this.story.slice(-2) == ". ") {
        // capitalize word after a period
        word = word[0].toUpperCase() + word.substring(1) + " ";
        this.story = this.story + word;
      } else if (word == "i") {
        // capitalize "I" e.g. "I am"
        word = word.toUpperCase() + " ";
        this.story = this.story + word;
      } else if (this.notSpacedPunctuation.includes(word)) {
        // remove spaces between single quotes, hyphens and dashes
        this.story = this.story.trim() + word;
      } else if (this.spacedPunctuation.includes(word)) {
        // add a space after question marks, periods, commas, colons, semicolons
        this.story = this.story.trim() + word + " ";
      } else {
        // add a space after every normal word
        word = word + " ";
        this.story = this.story + word;
      }
    },
    removeWord() {
      // remove last word from tokens
      this.storyTokens.pop();

      // split story into words and punctuation
      var words = this.story
        .split(/(,|\.|\!|\?|:|;|'|’|-|–|—)| /)
        .filter(Boolean);

      // removed word/punctuation
      var lastWord = words.pop();

      // remove lasWord from story
      this.story = this.story.trim().replace(new RegExp(lastWord + "$"), "");

      // add a space if lastWord was some punctuation mark
      if (
        this.spacedPunctuation.includes(lastWord) ||
        this.notSpacedPunctuation.includes(lastWord)
      ) {
        this.story = this.story + " ";
      }

      // recalculate suggestions
      this.getSuggestions();
    },
    reset() {
      this.nextWord = "";
      this.story = "";
      this.storyTokens = [];
      this.getSuggestions();
    },
    finishStory() {
      this.suggestions = null;
    },
    clearInput() {
      this.customWord = null;
    }
  }
};
</script>