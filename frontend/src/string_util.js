export function getClosestWord(str, pos) {
    // https://ourcodeworld.com/articles/read/223/how-to-retrieve-the-closest-word-in-a-string-with-a-given-index-in-javascript
    str = String(str);
    pos = Number(pos) >>> 0;
    var left = str.slice(0, pos + 1).search(/\S+$/),
        right = str.slice(pos).search(/\s/);
    if (right < 0) {
        return str.slice(left);
    }
    return str.slice(left, right + pos);
}
