/**
 * Created by kevinzeidler on 10/1/16.
 */
// viewport.js
// Author: Kevin Zeidler
// Description : I am a file that simply announces the state of the browser's viewport. My notifications can be
// subscribed to, and unsubscribed from. By default I detach subscriptions from nodes whose actions have been
// consumed. Don't use me to call events. I ain't no callback gurr. I ain't no callback gurr


function Point (x, y) {
    this.x = Number(x.toFixed(0)) || 0;
    this.y = Number(y.toFixed(1)) || 0;
}


var Viewport = (function() {
    var config = {
        updateInterval :     500,
        printUpdatesEvery :  1000,
        verboseModeEnabled : true,
        initialized :        false,
    };

    // var E = {
    //     all : (function() { return document.querySelectorAll("*"); })(),
    // };
    // Elements.topLeft = new Array(Elements.all.length);
    // Elements.bottomRight = new Array(Elements.all.length);
    //
    // $(document).height();
    var observing = [ "window.scrollX", "window.scrollY", "window.screenTop", "window.innerWidth",
                      "window.innerHeight" ];

    var cache = {

        pq : {
            0 : [ [ "window.scrollX", function () { return Number( window.scrollX.toFixed( 0 ) ); }, 0, 0, false,
                    [ 0, 1, 2 ] ],
                  [ "window.scrollY", function () { return Number( window.scrollY.toFixed( 0 ) ); }, 0, 0, false,
                    [ 0, 1, 2 ] ],
                  [ "window.screenTop", function () { return Number( window.screenTop.toFixed( 0 ) ); }, 0, 0, false,
                    [] ],
                  [ "window.innerWidth", function () { return Number( window.innerWidth.toFixed( 0 ) );}, 0, 0, false,
                    [ 1, 2 ] ],
                  [ "window.innerHeight", function () { return Number( window.innerHeight.toFixed( 0 ) ); }, 0, 0,
                    false, [ 1, 2 ] ] ],
            1 : [ [ "WindowTopLeft", function () {
                return new Point( window.scrollX + window.innerWidth / 2, window.scrollY +
                                                                          window.innerHeight / 2 )},
                    [ 0, 0 ], [ 0, 0 ], false, [ "belowFold" ] ],

                  [ "WindowCentroid", function () {
                      return new Point( window.scrollX + window.innerWidth / 2, window.scrollY +
                                                                                window.innerHeight / 2 )
                  }, [ 0, 0 ], [ 0, 0 ], false, [ "belowFold" ] ],
                  [ "WindowBottomRight", function () {
                      return new Point( window.scrollX + window.innerWidth, window.scrollY + window.innerHeight )
                  }, [ 0, 0 ], [ 0, 0 ], false, [ "belowFold" ] ] ]

        },

        // get : function ( datum, filter ) {
        //     var targetRegister = Number( NaN );
        //     sem                = [];
        //
        //     switch ( datum ) {
        //         case "scrollX":
        //             targetRegister = 0;
        //             break;
        //         case "scrollY":
        //             targetRegister = 1;
        //             break;
        //         case "screenTop":
        //             targetRegister = 2;
        //             break;
        //         case "innerWidth":
        //             targetRegister = 3;
        //             break;
        //         case "innerHeight":
        //             targetRegister = 4;
        //             break;
        //         case "lv1"
        //     }
        //     if ( this._data.hasOwnProperty( targetRegister ) ) {
        //         (filter.isNumeric()) ?
        //         sem.push( this.data[ targetRegister ][ filter ] ) :
        //         sem.push( this.data[ targetRegister ] );
        //         return sem.pop();
        //     }
        // }
    };

    var subscriptionsHaveUpdates = new Set();

    var subscriptions = [];

    function newObservables () {
        var newY = cached[ "window.innerHeight" ][ 3 ],
            oldY = cached[ "window.innerHeight" ][ 2 ],
            lst  = [];
        for ( var index = oldY; index < newY; index++ ) {
            if ( startsAt[ index ].length ) {
                startsAtIndex.map( function ( el ) {
                    lst.push( el );
                    return lst;
                } );
            }
        }
    }

    function init () {
        var DOMCache = document.querySelectorAll( "*" );
        var startsAt = new Array( DOMCache.length ),
            endsAt   = new Array( DOMCache.length );
        for ( el in DOMCache ) {
            console.log( el, DOMCache[ el ] );
            // startsAt[document.body.getBoundingClientRect().top - el.getBoundingClientRect().top] = el;
            // endsAt[document.body.getBoundingClientRect().top - el.getBoundingClientRect().bottom] = el;
        }

        cache.pq[ 0 ].map( function ( el, reg ) {
            // var functors = el[ 5 ];
            // if ( functors.length ) {    // Alert elements that are subscribed to this variable
            //     subscriptions[]
            // //     for ( var id = 0; id < subscribers.length; id++ ) {
            // //         StateAgents.notify(subscribers[ id ], [el[0], "begin"]);
            // //     }
            // // }
            window.setInterval( function () {
                var el  = cache.pq[0][reg];
                el[ 2 ] = el[ 3 ];
                el[ 3 ] = el[ 1 ].call();
                el[ 4 ] = Boolean( el[ 2 ] !== el[ 3 ] );

                if ( el[ 4 ] && el[ 5 ] && el[ 5 ].length ) {    // Alert elements that are subscribed to this variable
                    // console.log( "Broadcasting " + el[ 0 ] + "'s new value (" + el[ 3 ] +
                    //              ") to the subscribers list..." );
                    el[ 5 ].map( function ( subscriberIndex ) {
                        console.log( "Update available at " + subscriberIndex );
                        cache.pq[1][ subscriberIndex ][ 4 ] = true;
                        subscriptionsHaveUpdates.add( subscriberIndex );
                    } );
                }
            }, config.updateInterval );
        } );


        window.setInterval( function () {
            return (subscriptionsHaveUpdates && subscriptionsHaveUpdates.size > 0) ? (function () {
                var messages = cache.pq[ 1 ].map( function ( el, reg, subscriptions ) {
                    // var el                 = Viewport.cache.pq[ 1 ][ reg ],
                        var elementNeedsUpdate = el[ 4 ];
                    return (!elementNeedsUpdate) ? 0 : (function () {
                        var msg,
                            i = reg;
                        subscriptions[ i ][ 2 ] = subscriptions[ i ][ 3 ];
                        subscriptions[ i ][ 3 ] = subscriptions[ i ][ 1 ].call();
                        msg                     = {
                            to :   subscriptions[ i ][ 5 ],
                            from : subscriptions[ i ][ 0 ],
                            body : [ subscriptions[ i ][ 2 ], subscriptions[ i ][ 3 ] ],
                        };

                        StateAgents.submit(msg);
                        subscriptionsHaveUpdates.delete( i );
                        return msg;


                    })()
                } );
            })() : 0
        }, config.updateInterval );

        config.initialized = true;
        console.log("Changes: ", changed);
        console.log("Subscribers: ", updates);
        for ( var i = 0; i < changed.length; i++ ) {
            var valueWithUpdate = changed[ i ];
            for ( var j = 0; j < valueWithUpdate[ 5 ].length; j++ ) {
                var msgTo   = valueWithUpdate[ 5 ][ j ],
                    msgFrom = valueWithUpdate[ 0 ],
                    msgBody = valueWithUpdate[ 3 ],
                    msg     = [ msgFrom, msgBody ];
                updates.push( [ msgTo, msg ] );
            }
        }
        window.setInterval(function() {
            if (el[4]) {
                console.log(el);
            }
        }, config.printUpdatesEvery);

    }

    return {
        init : function () {
            if (config.initialized) { console.log("Viewport already initialized."); return; }
            init();

            console.log("Initialized Viewport!");

        },
        // load : function(lvl, row, col) {
        //     if ( typeof(col == "undefined") ) { return cache[lvl][row]}
        //     else {
        //         console.log("Loading " + row + ", " + col + "of the tier " + lvl + " cache....  " );
        //         console.log(cache[lvl][row][col]);
        //         return cache[ lvl ][ row ][col];
        //     }
        // },
        load : function ( datum, filter ) {
            console.log("cache value : ");
            console.log(cache);
            console.log(cache.pq);
            console.log(cache.pq[0]);
                    var cacheLevel = Number(NaN);
                    var targetRegister = Number( NaN );
                    sem                = [];

                    switch ( datum ) {
                        case "scrollX":
                            cacheLevel     = 0;
                            targetRegister = 0;
                            break;
                        case "scrollY":
                            cacheLevel     = 0;
                            targetRegister = 1;
                            break;
                        case "scrollTop":
                            cacheLevel     = 0;
                            targetRegister = 2;
                            break;
                        case "innerWidth":
                            cacheLevel     = 0;
                            targetRegister = 3;
                            break;
                        case "innerHeight":
                            cacheLevel     = 0;
                            targetRegister = 4;
                            break;
                        case "tier1":
                            cacheLevel     = 0;
                            targetRegister = Number( NaN );
                            break;
                        case "tier2":
                            cacheLevel = 1;
                            targetRegister = Number(NaN);
                            break;
                    }
                    console.log ("Requested the " + cacheLevel + " data cache at offset " + targetRegister );
                    console.log ("  with supplied args " + datum, filter + "...");
                    console.log(cache[cacheLevel]);

                    if (isNaN(targetRegister)) {
                        if ( isNaN( cacheLevel ) ) {
                            return "Null pointer." + cache.pq;
                        } else {
                            return "Returning the entire cache level " + cache.pq.cacheLevel;
                        }
                    } else {
                        return "Here's the requested row: " + cache.pq.cachelevel.targetRegister

                        }
                        // sem.push( cache.pq[ targetRegister ][ filter ] ) :
                        // sem.push( cache.pq[ targetRegister ] );
                        // return sem.pop();
                    }
                // }
            }
        })();



/**
 * Author: Jason Farrell
 * Author URI: http://useallfive.com/
 *
 * Description: Checks if a DOM element is truly visible.
 * Package URL: https://github.com/UseAllFive/true-visibility
 */
Element.prototype.isVisible = function() {
    'use strict';
    /**
     * Checks if a DOM element is visible. Takes into
     * consideration its parents and overflow.
     *
     * @param (el)      the DOM element to check if is visible
     *
     * These params are optional that are sent in recursively,
     * you typically won't use these:
     *
     * @param (t)       Top corner position number
     * @param (r)       Right corner position number
     * @param (b)       Bottom corner position number
     * @param (l)       Left corner position number
     * @param (w)       Element width number
     * @param (h)       Element height number
     */
    function _isVisible(el, t, r, b, l, w, h) {
        var p = el.parentNode,
            VISIBLE_PADDING = 2;
        if (!_elementInDocument(el)) {
            return false;
        }
        //-- Return true for document node
        if (9 === p.nodeType) {
            return true;
        }
        //-- Return false if our element is invisible
        if (
            '0' === _getStyle(el, 'opacity') ||
            'none' === _getStyle(el, 'display') ||
            'hidden' === _getStyle(el, 'visibility')
        ) {
            return false;
        }
        if (
            'undefined' === typeof(t) ||
            'undefined' === typeof(r) ||
            'undefined' === typeof(b) ||
            'undefined' === typeof(l) ||
            'undefined' === typeof(w) ||
            'undefined' === typeof(h)
        ) {
            t = el.offsetTop;
            l = el.offsetLeft;
            b = t + el.offsetHeight;
            r = l + el.offsetWidth;
            w = el.offsetWidth;
            h = el.offsetHeight;
        }
        //-- If we have a parent, let's continue:
        if (p) {
            //-- Check if the parent can hide its children.
            if (('hidden' === _getStyle(p, 'overflow') || 'scroll' === _getStyle(p, 'overflow'))) {
                //-- Only check if the offset is different for the parent
                if (
                    //-- If the target element is to the right of the parent elm
                l + VISIBLE_PADDING > p.offsetWidth + p.scrollLeft ||
                //-- If the target element is to the left of the parent elm
                l + w - VISIBLE_PADDING < p.scrollLeft ||
                //-- If the target element is under the parent elm
                t + VISIBLE_PADDING > p.offsetHeight + p.scrollTop ||
                //-- If the target element is above the parent elm
                t + h - VISIBLE_PADDING < p.scrollTop
                ) {
                    //-- Our target element is out of bounds:
                    return false;
                }
            }
            //-- Add the offset parent's left/top coords to our element's offset:
            if (el.offsetParent === p) {
                l += p.offsetLeft;
                t += p.offsetTop;
            }
            //-- Let's recursively check upwards:
            return _isVisible(p, t, r, b, l, w, h);
        }
        return true;
    }
    //-- Cross browser method to get style properties:
    function _getStyle(el, property) {
        if (window.getComputedStyle) {
            return document.defaultView.getComputedStyle(el, null)[property];
        }
        if (el.currentStyle) {
            return el.currentStyle[property];
        }
    }
    function _elementInDocument(element) {
        while (element = element.parentNode) {
            if (element == document) {
                return true;
            }
        }
        return false;
    }
    return _isVisible(this);
};