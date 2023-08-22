const rpc = require("discord-rpc");
const client = new rpc.Client({ transport: 'ipc' });
const config = require('./config.json');

client.login({ clientId: config.ClientID }).catch(console.error);

client.on('ready', () => {
    console.log('[DEBUG] Presence now active!')
    console.log('[WARN] Do not close this Console as it will terminate the rpc')
    console.log('=================== Error Output ===================')

    const activity = {
        pid: process.pid,
        activity: {
            details: config.Details,
            state: config.State,
            timestamps: {
                start: Date.now()
            },
            assets: {}
        }
    };

    if (config.LargeImage) {
        activity.activity.assets.large_image = config.LargeImage;
    }
    if (config.LargeImageText && config.LargeImage) {
        activity.activity.assets.large_text = config.LargeImageText;
    }
    if (config.SmallImage) {
        activity.activity.assets.small_image = config.SmallImage;
    }
    if (config.SmallImageText && config.SmallImage) {
        activity.activity.assets.small_text = config.SmallImageText;
    }
    if (config.Button1 && config.Url1) {
        activity.activity.buttons = [{
            label: config.Button1,
            url: config.Url1
        }];
    }
    if (config.Button2 && config.Url2) {
        activity.activity.buttons = activity.activity.buttons || [];
        activity.activity.buttons.push({
            label: config.Button2,
            url: config.Url2
        });
    }

    client.request('SET_ACTIVITY', activity);
});
