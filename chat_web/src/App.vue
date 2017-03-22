<template>
  <div id="app" class="app-wrap">
    <!--<img src="./assets/logo.png">-->
    <!--<router-view></router-view>-->
    <div class="uid">
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
        v-text="show_uid"
      >Prompt12</md-button>
    </div>

    <div class="msg-list">
      <md-list>
        <md-list-item v-for="item in msgs" :key="item.time" track-by="$index">
          <p class="msg-wrap">
            <span style="font-weight: bold; color: #0000FF;">{{ item.uid }}: </span>{{ item.msg }}
            <br>
            <small style="">{{ item.time }}</small>
          </p>
        </md-list-item>
      </md-list>
    </div>

    <div class="send" @keyup.enter="clickSend()">
      <md-input-container md-inline class="md-input-invalid">
        <label>You can Input</label>
        <md-input v-model="text" @keyup.enter="clickSend()"></md-input>
      </md-input-container>
      <md-button
        class="md-raised md-accent"
        @click.native="clickSend()"
      >Send</md-button>
    </div>

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
    text: '',
    msgs: [],
    ws: null
  }),
  computed: {
    show_uid () {
      return 'id: ' + (this.uid ? this.uid : 'Not set')
    }
  },
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
    },
    sendMsg(msg) {
      this.ws.send(JSON.stringify({
        'uid': this.uid,
        'msg': msg
      }))
    },
    clickSend() {
      try {
        this.sendMsg(this.text)
      } catch (err) {
        console.log(err)
      } finally {
        this.text = ''
//        let li = $.getElementsByClassName('msg-list')
//        li.scrollTo(0, li.scrollHeight)
//        window.scrollTo(0,document.body.scrollHeight)
//        window.scrollTo(0, $(window).height() + $(window).scrollTop())
      }
    },
    keepUid() {
      setTimeout(() => {
        if (this.uid == '' | this.uid == null) {
          this.openDialog('dialog-uid')
        }
        this.keepUid()
      }, 1000)
    },
    initWs() {
      setTimeout(() => {
        if (this.uid != '' & this.ws == null) {
          try {
            let ws = new WebSocket("ws://" + window.location.host + '/chatws')
//            let ws = new WebSocket('ws://127.0.0.1/chatws')
//            if (ws) {this.ws = ws} else if (ws2) {this.ws = ws2}
            this.ws = ws
            this.ws.onopen = () => {
                console.log('WebSocket connected', this.uid)
                localStorage.setItem('uid', this.uid)
                this.sendMsg('Online')
            }
            this.ws.onmessage = (evt) => {
                this.msgs.push(JSON.parse(evt.data))
                this.$nextTick(() => {
                  window.scrollTo(0,document.body.scrollHeight)
                })
            }
            this.ws.onerror = (err) => {
                console.log(err)
            }
          }
          catch (err) {
              console.log(err)
          }
        }
        this.initWs()
      }, 2000)
    }
  },
  created () {
//    if (localStorage.getItem('uid')) {
//      this.uid = localStorage.getItem('uid')
//    }
    this.keepUid()
    this.initWs()
  }
}

</script>

<style>
  .app-wrap {
    /*overflow: hidden;*/
  }
  .uid {
    position: fixed;
    top: 0px;
    left: 10px;
    z-index: 10;
    background: white;
    width: 100%;

  }
  .msg-list {
    position: relative;
    width: 100%;
    top: 50px;
    /*margin-top: 60px;*/
    margin-bottom: 124px;
    /*overflow: auto;*/
    /*height: 60%;*/
    /*top: 60px;*/
    /*bottom: 130px;*/
  }
  .msg-wrap {
    word-wrap: break-word;
    word-break: break-all;
  }
  .send {
    position: fixed;
    background: white;
    /*left: 15px;*/
    margin-left: 15px;
    bottom: 0px;
    width: 100%;
    z-index: 10;
  }
</style>
