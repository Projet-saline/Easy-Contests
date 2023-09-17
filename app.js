'use strict';

const express = require('express');
const app = express();
const cors = require('cors');


const port = 4000;
app.use(cors());

const woodwind = '/woodwind';
const brass = '/brass';
const strings = '/strings';
const keyboard = '/keyboard';
const percusion = '/percusion';
const voice = '/voice';
const chamber = '/chamber';
const direction = '/direction';
const composition = '/composition';
const craft = '/craft';

const woodwindRoute = require('./src/routes/woodwind');
const brassRoute = require('./src/routes/brass');
const stringsRoute = require('./src/routes/strings');
const keyboardRoute = require('./src/routes/keyboard');
const percusionRoute = require('./src/routes/percusion');
const voiceRoute = require('./src/routes/voice');
const chamberRoute = require('./src/routes/chamber');
const directionRoute = require('./src/routes/direction');
const compositionRoute = require('./src/routes/composition');
const craftRoute = require('./src/routes/craft');

app.use(woodwind,woodwindRoute);
app.use(brass,brassRoute);
app.use(strings,stringsRoute);
app.use(keyboard,keyboardRoute);
app.use(percusion,percusionRoute);
app.use(voice,voiceRoute);
app.use(chamber,chamberRoute);
app.use(direction,directionRoute);
app.use(composition,compositionRoute);
app.use(craft,craftRoute);

app.listen(port, () => {
  console.log(`Server listen on port : ${port}`);
});