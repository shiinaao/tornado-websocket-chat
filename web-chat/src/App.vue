<template>
  <div id="app">
    <!--<img src="./assets/logo.png">-->
    <!--<router-view></router-view>-->

    <md-dialog-prompt
      :md-title="prompt.title"
      :md-ok-text="prompt.ok"
      :md-cancel-text="prompt.cancel"
      v-model="uid"
      @open="onOpen"
      @close="onClose"
      ref="dialog-uid">
    </md-dialog-prompt>

    <md-button
      class="md-primary md-raised"
      @click.native="openDialog('dialog-uid')"
      v-text="uid"
    >Prompt12</md-button>
  </div>
</template>
s
<script>
import 'vue-material/dist/vue-material.css'
import $ from 'n-zepto'
export default {
  name: 'app',
    data: () => ({
    prompt: {
      title: 'What\'s your name?',
      ok: 'Done',
      cancel: 'Cancel',
      maxlength: 30,
    },
    uid: '',
    hashid: null,
    msg: [],
    wscon: null
  }),
  methods: {
    openDialog(ref) {
      this.$refs[ref].open()
    },
    closeDialog(ref) {
      this.$refs[ref].close()
    },
    onOpen() {
      console.log('Opened')
    },
    onClose(type) {
      console.log('Closed', type)
      this.userLogin()

    },
    userLogin() {
      $.post('http://127.0.0.1/chat', {'uid': this.uid}, (response) => {
//        console.log(response)
        this.hashid = response.hashid
      })
    },
    keepUid() {
      setTimeout(() => {
        if (this.uid == '' | this.uid == null) {
          console.log('open')
          this.openDialog('dialog-uid')
        }
        this.keepUid()
      }, 1000)
    },
    conWs() {
      setTimeout(() => {
        if (this.uid != null & this.wscon == null) {
//          let ws = new WebSocket("ws://" + window.location.host + '/chatws')
          try {
            let ws = new WebSocket('ws://127.0.0.1/chatws')
            this.wscon = 1
            ws.onopen = () => {
                ws.send(this.uid + '#login')
            }
            ws.onmessage = (evt) => {
                console.log(evt.data)
                this.msg.push(evt.data)
            }
            ws.onerror = (err) => {
                console.log(err)
            }
            ws.send('Test data')
          }
          catch (err) {
              console.log(err)
          }


        }
        this.conWs()
      }, 2000)
    }
  },
  created () {
    if (localStorage.getItem('uid')) {
      this.uid = localStorage.getItem('uid')
    }
    this.keepUid()
    this.userLogin()
    this.conWs()
  }
}
</script>

<style>

</style>
