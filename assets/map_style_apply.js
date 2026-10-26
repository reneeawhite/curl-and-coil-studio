// Plotly.js 4.1.1 (bundled with this Dash version) only accepts a fixed set of
// named map styles ("carto-voyager", "open-street-map", ...) through the figure's
// own layout.map.style attribute - an arbitrary style URL/object there gets
// silently rejected and replaced with the default. The same Plotly.relayout()
// API does accept a full custom style *object* at runtime, so this polls for the
// Find a Stylist map and (re)applies our recolored style - including after every
// filter change, since each one hands the graph a brand-new figure that resets
// back to the rejected default.
(function () {
  var STYLE_NAME = "Restful Roots (recolored CARTO Positron)";
  var styleObjPromise = null;

  function getStyleObj() {
    if (!styleObjPromise) {
      styleObjPromise = fetch("/assets/map_style.json").then(function (r) {
        return r.json();
      });
    }
    return styleObjPromise;
  }

  function currentlyCustom(gd) {
    try {
      return gd._fullLayout.map.style && gd._fullLayout.map.style.name === STYLE_NAME;
    } catch (e) {
      return false;
    }
  }

  function tick() {
    var outer = document.getElementById("provider-map");
    if (!outer) return;
    var gd = outer.querySelector(".js-plotly-plot");
    if (!gd || !gd._fullLayout || !gd._fullLayout.map) return;
    if (currentlyCustom(gd) || gd._curlCoilApplying) return;
    gd._curlCoilApplying = true;
    getStyleObj()
      .then(function (styleObj) {
        return window.Plotly.relayout(gd, { "map.style": styleObj });
      })
      .catch(function () {})
      .then(function () {
        gd._curlCoilApplying = false;
      });
  }

  setInterval(tick, 400);
})();
