import { createApp } from 'vue'
import { createPinia } from 'pinia'
import {
  Button, Cell, CellGroup, Field, Form, Tab, Tabs, Card,
  Tag, Stepper, Empty, Icon, Rate, Dialog, Notify, Toast,
  Image as VanImage, Badge, Popup, ActionSheet, Loading,
  Divider, Search, Uploader, Picker, Switch,
} from 'vant'
import 'vant/lib/index.css'

import App from './App.vue'
import router from './router'
import { useUserStore } from '@/stores/user'

const app = createApp(App)

// 按需注册 Vant 组件
app.use(Button)
app.use(Cell)
app.use(CellGroup)
app.use(Field)
app.use(Form)
app.use(Tab)
app.use(Tabs)
app.use(Card)
app.use(Tag)
app.use(Stepper)
app.use(Empty)
app.use(Icon)
app.use(Rate)
app.use(Dialog)
app.use(Notify)
app.use(Toast)
app.use(VanImage)
app.use(Badge)
app.use(Popup)
app.use(ActionSheet)
app.use(Loading)
app.use(Divider)
app.use(Search)
app.use(Uploader)
app.use(Picker)
app.use(Switch)

app.use(createPinia())
app.use(router)

// 恢复用户登录状态
const userStore = useUserStore()
userStore.restore()

app.mount('#app')
