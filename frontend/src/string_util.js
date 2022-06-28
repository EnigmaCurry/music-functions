export function get_closest_word(str, pos) {
  // https://ourcodeworld.com/articles/read/223/how-to-retrieve-the-closest-word-in-a-string-with-a-given-index-in-javascript
  var str = String(str);
  var pos = Number(pos) >>> 0;
  var left = str.slice(0, pos + 1).search(/\S+$/),
    right = str.slice(pos).search(/\s/);
  if (right < 0) {
    return str.slice(left);
  }
  return str.slice(left, right + pos);
}

export function get_next_word_position(str, current_pos, direction) {
  var str = String(str);
  var current_pos = Number(current_pos) >>> 0;
  if (typeof direction === "undefined") direction = 1;
  const regexp = /[^ \n]+/g;
  const chords = [...str.matchAll(regexp)];
  const stops = wrapped_index_array(
    chords.map((i) => {
      return i.index + i[0].length;
    })
  );
  console.log(stops);

  function next_stop(pos, stops, direction) {
    if (typeof direction === "undefined") direction = 1;
    if (stops.includes(pos)) {
      return stops[(stops.indexOf(pos) + direction) % stops.length];
    } else {
      let new_pos = pos;
      while (new_pos >= 0 && new_pos <= str.length) {
        new_pos += direction;
        if (stops.includes(new_pos)) {
          return stops[(stops.indexOf(new_pos) + direction) % stops.length];
        }
      }
      if (direction > 0) {
        return stops[0];
      } else {
        return stops[-1];
      }
    }
  }

  return next_stop(current_pos, stops, direction);
}

function wrapped_index_array(arr) {
  // Return a python-like array that can index from the end with -1, -2, ...
  return new Proxy(arr, {
    get(target, prop) {
      if (!isNaN(prop)) {
        prop = parseInt(prop, 10);
        if (prop < 0) {
          prop += target.length;
        }
      }
      return target[prop];
    },
  });
}
