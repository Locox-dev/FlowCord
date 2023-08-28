const rpc = require("discord-rpc");
const client = new rpc.Client({ transport: 'ipc' });
const config = require('./JSON/richpresence.json');

var selectedConfigName = ""
process.argv.forEach(function (val, index, array) {
    if(index == 2) {
        selectedConfigName = val;
    }
    if(index > 2) {
        selectedConfigName = selectedConfigName + " " + val;
    }
});

const selectedConfig = config[selectedConfigName];

if (!selectedConfig) {
    console.error(`Configuration "${selectedConfigName}" not found in settings.json`);
    process.exit(1);
}

client.login({ clientId: selectedConfig.ClientID }).catch(console.error);

client.on('ready', () => {
    console.log('[DEBUG] Presence now active!')

    const activity = {
        pid: process.pid,
        activity: {
            timestamps: { 
                start: Date.now()
            },
            assets: {}
        }
    };

    if (selectedConfig.Details) {
        activity.activity.details = selectedConfig.Details;
    }
    if (selectedConfig.State) {
        activity.activity.state = selectedConfig.State;
    }
    if (selectedConfig.LargeImage) {
        activity.activity.assets.large_image = selectedConfig.LargeImage;
    }
    if (selectedConfig.LargeImageText && selectedConfig.LargeImage) {
        activity.activity.assets.large_text = selectedConfig.LargeImageText;
    }
    if (selectedConfig.SmallImage) {
        activity.activity.assets.small_image = selectedConfig.SmallImage;
    }
    if (selectedConfig.SmallImageText && selectedConfig.SmallImage) {
        activity.activity.assets.small_text = selectedConfig.SmallImageText;
    }
    if (selectedConfig.Button1 && selectedConfig.Url1) {
        activity.activity.buttons = [{
            label: selectedConfig.Button1,
            url: selectedConfig.Url1
        }];
    }
    if (selectedConfig.Button2 && selectedConfig.Url2) {
        activity.activity.buttons = activity.activity.buttons || [];
        activity.activity.buttons.push({
            label: selectedConfig.Button2,
            url: selectedConfig.Url2
        });
    }

    client.request('SET_ACTIVITY', activity);
});
