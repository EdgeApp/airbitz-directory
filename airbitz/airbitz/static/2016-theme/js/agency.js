/**
 * Created by kevinzeidler on 10/1/16.
 */

/* Consumes the messages produced by viewport.js */


// The current implementation uses atom to eliminate the Immutable.js dependency 
var ratom = Immutable.List();
var atom = {
    'initialized' :           false,
    'messageQueueHasUpdate' : false,
    'classIdentifier' :       'stateful',
    'channels' :              {
        'belowFold' : [],
        'currentObservables' : []
    },
    'nodeList' :              [],
    'message' :               {
        'qPointerA' : 0,
        'qPointerB' : 0,
        'q' :         new Array( 10 ).fill( null )
    }
}


var StateAgents = (function() {

    function querySelectAllByClass ( classname ) {
        var selector        = "",
            results         = "",
            currentChannels = Object.keys( atom.channels );
        if ( classname && classname.length && typeof(classname == "string")) {
         	if (classname[ 0 ] != ".") {
            	selector = "." + classname;
            } else {
            	selector = classname;
            }
        } else {
        	console.log("Argument to querySelectAllByClass must be a non-empty string")
        }
        results = document.querySelectorAll( selector );
        console.log( "I found " + results.length + " results with selector " + selector );
        for ( var i = 0; i < results.length; i++ ) {
            console.log( "Result " + i + ": " + results[ i ] );
            atom.nodeList.push( results[ i ] );
            for ( klazz in currentChannels ) {
                console.log( "Checking if it's a " + currentChannels[ klazz ] + " subscriber." );
                if ( results[ i ].hasOwnProperty( 'classList' ) && results[ i ][ currentChannels[ klazz ] ] ) {
                    console.log( "It is!" );
                } else {
                    console.log( "Doesn't look like it." );
                }
            }
            console.log( atom );
        }
        console.log( "Query complete. Final state of the app atom: " );
        console.log( atom );
        console.log( atom.nodeList );
        return atom;
    }

    function init () {
        var channels, myClasses, subscriptionsFound, finishSubscribing;

        console.log( "Value of atom on init: " + atom );

        if ( atom && !atom.initialized ) {
            channels = new Set( Object.keys( atom.channels ) );
            data     = querySelectAllByClass( atom.classIdentifier );
        }

        console.log( "Atom now:" );
        console.log( atom );

        atom.initialized = true;
        return atom;

    }

    return {

        // atom : function () {
        //     console.log( "Value of the atom: ");
        //     console.log( atom );
        // },
        size :        function () {
            return (atom.initialized && atom.nodeList && atom.nodeList.length ) ? 0 : atom.nodeList.size();
        },
        submit :      function ( msg ) {
            if ( !atom.initialized ) {
                this.init();
            }
            atom.message.q[ atom.message.qPointerB ] = msg;
            atom.message.qPointerB += 1;
            console.log( atom );
            return atom;

        },
        processNext : function ( newState ) {
            if (newState.message.qPointerA === newState.message.qPointerB) { return }
            else if (newState.message.qPointerA < newState.message.qPointerB) {
                var msg = newState.message.q[newState.message.qPointerA];
                if (typeof(msg['to']) == "array") {
                    msg['to'] = msg[ 'to' ];
                }
                for (var i = 0; i < newState.channels[msg]; i++) { msg[i]; }


            }
            if ( newState.message.qPointerA < newState.message.qPointerB ) {
                var nextMessage = newState.message.q[ newState.message.qPointerA ];
                newState.message.qPointerA += 1;
                // console.log( "Processed " + nextMessage + ". Value of front pointer: " + newState.message.qPointerA );
                newState.messageQueueHasUpdate =
                    (function () { return newState.message.qPointerA < newState.message.qPointerB })();

                // var ms
                for ( var i = 0; i < newState.channels[ msg['to']]; i++ ) {
                    var nodeNeedsUpdate = newState.channels[ msg['to'] ];
                    newState.channels[ msg['to'] ][i] = {['$messages'] : msg['body']};
                    console.log( nodeNeedsUpdate );
                }
            }
            return atom;

        },
        init :        function () {
            var state       = [];
            initializedAtom = init();
            state.push( initializedAtom );
            console.log( "Atom/state:" );
            console.log( initializedAtom );
            console.log( state );
            window.setInterval( function () {
                atom = initializedAtom;
                if ( atom.message.qPointerA < atom.message.qPointerB ) {
                    console.log( "Message queue has an update!" );
                    atom.messageQueueHasUpdate = true;
                    this.state                 = StateAgents.processNext( atom );
                    atom                       = this.state;
                    console.log("New observables:");
                    return atom;
                }
                else {
                    return;
                }
            }, 50 );
        },
        addClasses :  function ( newState ) {

            for ( var i = 0; i < newState.nodeList.length; i++ ) {
                var kla$zzy = newState.nodeList[ i ];
                myClasses   = newState.nodeList[ i ].classList.value.split( " " );
                myClasses   = myClasses.filter( function ( k ) { return (newState.channels.hasOwnProperty( k )) ? (function() {
                    newState.channels[k].push({ el : kla$zzy, messages: []});

                }) :

                                                                        [] } );
                console.log(myClasses)

            }

        },
        notifySubscribers : function(klazz, msg, newState) {
            var targets = newState.channels[klazz].forEach(function(x) { x.messages.push(msg) })
        }
    }
})();


StateAgents.init();

StateAgents.addClasses(atom);

// var StateAgents = (function() {
//
//     var data                   = {},
//         root,
//         subscriberLists        = {},
//         domNodeList            = [],
//         initialized = false,
//         messageQueue           = {
//             frontPtr : 0,
//             rearPtr : 0,
//             data : new Array( 20 ).fill( null ),
//             sources : [ "WindowTopLeft", "WindowCentroid", "WindowBottomRight" ]
//         },
//         classTag               = "stateful",
//         subscriberCount        = 0,
//         messageQueueDispatcher = {
//             initialized : false,
//             busy : false,
//             ref : [ "" ],
//             lastUpdate : false
//         };
//
//     function buildSubscriptionIndex ( className ) {
//         var filtered = [];
//         for ( entry in data ) {
//             if ( data[ entry ][ idx ] && data[ entry ][ idx ].hasClass( className ) ) {
//                 filtered.push( entry )
//             }
//         }
//         subscriberLists[ className ] = filtered;
//     }
//
//     function getAll ( msg ) {
//         if ( !msg ) {
//             return data;
//         } else if ( msg === "keys" ) {
//             return Object.keys( data );
//         } else {
//             return "Unknown message: " + msg;
//         }
//     }
//
//     function getBusy () {
//         return data.filter( function ( el ) { return el.messages.length; } );
//     }
//
//     function getSome ( selected ) {
//         return data.filter( function ( el ) { return el.status = selected} )
//     }
//
//     function getID ( _id ) {
//         var selected      = false,
//             currentTarget = 0;
//         while ( !selected && selected < data.length ) {
//             selected = (data[ currentTarget ].id === _id);
//             selected += 1;
//         }
//         return (selected) ? selected : [];
//     }
//
//     function addSelector ( node ) {
//         if ( node.hasId ) {
//             node.hashVal = node.id;
//         }
//         node.altSelector = domNodeList.indexOf( node );
//         if ( node.altSelector ) {
//             node.hasAltSelector = true;
//             node.hashVal        = altSelector;
//         }
//         return node;
//     }
//
//     function addSubscriber ( k, el ) {
//
//        function() newSubscriber       = {
//             status :       0,
//             keyedTo :      k,
//             idx :          el,
//             hasId :        function() { return this.idx.hasOwnProperty('id'); },
//
//             id :           function() { return this.idx.id; },
//             jq :           "",
//             hashVal :      "",
//             subscribedTo : [],
//             messages :     [],
//             processed :    []
//         };
//
//
//         return data
//     }
//
//     function removeSubscriber ( k, el ) {
//         console.log( "No. Much danger. Do not do. Wow." );
//     }
//
//     function subscribeAll ( msg ) {
//         var newSubscribers = document.querySelectorAll( msg );
//         for ( var i = 0; i < newSubscribers.length; i++ ) {
//             if ( !newSubscribers[ i ] in Object.keys(data) ) {
//                 console.log( "Subscribing" + newSubscribers[ i, newSubscribers[i] ] );
//                 data[i] = addSubscriber( newSubscribers[ i ] );
//                 console.log(data);
//                 console.log(data[i]);
//                 console.log(newSubscribers[i]);
//             }
//         }
//         return "Subscribed."
//         return data;
//     }
//
//     function notifySubscriber ( el, msg ) {
//         if ( data[ el ] ) {
//             data[ el ].messages.push( msg );
//             console.log( "Notified " + el + " of state change to " + msg[ 0 ] );
//             console.log( data[ el ] );
//             return true;
//         }
//
//         console.log( "Element " + el + " isn't subscribed." );
//         data = addSubscriber( el );
//     }
//
//     function getCallerSignature ( id ) {
//         return "generic"
//     }
//
//     // function matchesDeclaredSignature(sender, body) {
//     //     var callerSignature = getCallerSignature(sender),
//     //         inspections;
//     //     switch (callerSignature) {
//     //         case "generic" :
//     //             var inspections = [ function() { return Boolean( typeof(body) === "array" ) })
//     //                 , Boolean( body.length === 2 )
//     //                 , Boolean( typeof(body[ 0 ]) === "array" )
//     //                 , Boolean( typeof(body[ 1 ]) === "array" )
//     //                 , Boolean( body[ 0 ].length === 2 )
//     //                 , Boolean( body[ 1 ].length === 2 ),
//     //                 , Boolean( typeof(body[ 0 ][ 0 ]) === "number" && typeof(body[ 0 ][ 1 ]) === "number" )
//     //                 , Boolean( typeof(body[ 1 ][ 0 ]) === "number" && typeof(body[ 1 ][ 1 ]) === "number" ) ];
//     //     }
//     //
//     //     }
//     // }
//
//     function fromKnownSender ( sender ) {
//         return messageQueue.sources.filter( function ( x ) { return x === sender} );
//     }
//
//     function validateHeaders ( index ) {
//         var msg = messageQueue[ index ];
//         // messageQueue.data[index].delivered = false;
//         // messageQueue.data[status] = parseInt([msg, msg.hasOwnProperty('to')
//         //     , msg.hasOwnProperty('from') && typeof(msg['from'] === "string") && fromKnownSender (msg['from'])
//         //     , msg.hasOwnProperty('body') &&  typeof(msg[body] === "array") && msg[body].length === 2 && typeof(msg[body][0]) === "array" && msg[body][0].length === 2 && typeof(msg[body][1]) == "array" && msg[body][1].length === 2 && typeof(msg[body][0][0]) == "number"  && typeof(msg[body][0][1]) == "number" && typeof(msg[body][1][0]) == "number" && typeof(msg[body][1][0]) == "number",
//         //       msg.delivered].join(""),2);
//         //
//         //
//         // (data[status] === 30) ? (function() {
//         //     console.log("Message in position " + index + " ready for broadcast. The message:");
//         //     console.log(msg)
//         //     return true;
//         // })() : (function() {
//         //     console.log("The message doesn't match the expected content signature. Error code: " + data[status]);
//         //     return false;
//         // })();
//         return true;
//
//     }
//
//     function enqueue ( msg ) {
//         var bufferSize                              = messageQueue.size;
//         msg.sent                                    = false;
//         msg.status                                  = 0;
//         messageQueue.rearPtr += 1;
//         messageQueue.data[messageQueue.rearPtr] = msg;
//         console.log( messageQueue );
//
//         if ( messageQueue.rearPtr > bufferSize/2) {
//             for (var i = 0; i < bufferSize/2; i++) {
//                 messageQueue.push(null);
//             }
//         }
//
//     }
//
//     function init () {
//         if (!this.init) {
//             subscribers = document.querySelectorAll(".stateful");
//
//
//             for ( var i = 0; i < subscribers.length; i++ ) {
//                 data[i] = addSubscriber( subscribers[ i ], i );
//
//
//             }
//
//             initialialized = true;
//             console.log(data);
//             return data;
//         }
//         else { console.log("Already initialized")}
//
//     }
//
//
//         //    window.setInterval(function() {
//         //         console.log("Can process? " + validateHeaders(canProcess));
//         //         console.log("Ids of this message's subscribers? " + subscriberLists["belowFold"]);
//         //         if (messsageQueue.frontPtr === messageQueue.rearPtr) { return false; }
//         //         else {
//         //             var canProcess = validateHeaders(frontPtr);
//         //             return subscriberLists['belowFold'];
//         //         }
//         //     }, 1000);
//         // }
//
//         return {
//             init : function() {
//                 if ( initialized ) { return "Already initialized" }
//                 else {
//                     init();
//
//                         return window.setInterval (function() {
//                             console.log(ratom);
//                             console.log(StateAgents.messageQueue.frontPtr != StateAgents.messageQueue.rearPtr);
//                             return (StateAgents.messageQueue.frontPtr != StateAgents.messageQueue.rearPtr) ? (function() {
//                                 var newState = ratom.push( StateAgents.messageQueue.data[ StateAgents.messageQueue.frontPtr] );
//                                 console.log( "State of ratom after push: " );
//                                 console.log( newState );
//                                 return (function() { return ratom =  newState; })();
//                             })(): console.log( "StateAgents up to date. Front pointer is at " + StateAgents.messageQueue.frontPtr);
//
//                         },1000);
//
//
//                 }
//             },
//             root :          root,
//             data :          function() {
//                 var d = data;
//                 var toString = JSON.stringify(d);
//                 return toString;
//             },
//             all :           function () { return getAll(); }(),
//             list :          function () { return getAll( 'keys' ); }(),
//             busy :          getBusy,
//             some :          getSome,
//             add :           addSubscriber,
//             subscribeAll :  subscribeAll,
//             submit :        enqueue,
//             count :         Object.keys( data ).length,
//             notify :        notifySubscriber,
//             subscriberLists : subscriberLists,
//             messageQueue :     messageQueue,
//             subscribersTo : function ( className ) {
//                 var subscriptionIndex = buildSubscriptionIndex(className);
//                 console.log( subscriptionIndex );
//                 return subscriptionIndex;
//                 // if (subscriptionIndex[className] && subscriptionIndex[className].length) {
//                 //     return subscriptionIndex[className];
//                 // } else {
//                 //     subscriptionIndex[className] = buildSubscriptionIndex(className);
//                 //     console.log("Update finished. Here are the elements subscribed to " + className + ":");
//                 //     return subscribers[className];
//                 // }
//
//             }
//         }
//
//     })();
//
//
// window.setInterval( function () {
//     if (StateAgents.messageQueue.frontPtr !== StateAgents.messageQueue.rearPtr) {
//         console.log( "Next message in the queue: " );
//         StateAgents.messageQueue.frontPtr += 1;
//         console.log( JSON.stringify( StateAgents.messageQueue.data[ StateAgents.messageQueue.frontPtr ] ) );
//         return StateAgents;
//
//     }
// }, 16 );
//
// StateAgents.init()