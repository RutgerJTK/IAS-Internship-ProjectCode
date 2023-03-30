console.log('hello world');

const { EventEmitter } = require('events');
const EventEmitter = new EventEmitter();

EventEmitter.on('lunch', () => {
    console.log('yummie')
})

EventEmitter.emit('lunch');
EventEmitter.emit('lunch');

// process.on('exist', function() {

//     // do something!

// })