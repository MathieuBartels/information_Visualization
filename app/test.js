source_data = source["data"]

// subtraction function where we subtract a value from an array
const subtract = function(array, value) {return array.map( array_at_i => array_at_i -value)}

// slider array values
const slider_array = sliders.map(slider => slider['properties']['value']['spec']['value']);
// slider array names
const slider_idx_to_name = sliders.map(slider => slider['attributes']['title']);

// source data for all images
const source_vectors = slider_idx_to_name.map(name => source_data[name]);

// for each row of features subtract the slider value
const subtracted_feature_matrix = source_vectors.map(function(v, i) { return subtract(v,  slider_array[i])});

var scores = new Array(220)
for (i = 0; i < 220; i++) {
    scores[i] = Math.abs(subtracted_feature_matrix.map(value => value[i]).reduce((a,b) => a+b, 0))
} 

indexedScores = scores.map(function(e,i){return {ind: i, val: e}});
// sort index/value couples, based on values
indexedScores.sort(function(x, y){return x.val > y.val ? 1 : x.val == y.val ? 0 : -1});
// make list keeping only indices
const rank = indexedScores.map(function(e){return e.ind + 1});

source["data"]['rank'] = rank 
source["data"]["x1"] = rank

const x_range = per_row * image_width
const y_range = 220 / per_row * image_height

source["data"]['x1'] = source["data"]['rank'].map(value => (value - 1) % per_row)
source["data"]['y1'] = source["data"]['rank'].map(value => y_range - Math.floor((value - 1) / per_row))
source["data"]['x2'] = source["data"]['rank'].map(value => (value - 1) % per_row + image_width) 
source["data"]['y2'] = source["data"]['rank'].map(value => y_range - Math.floor((value - 1) / per_row) - image_height) 

source.change.emit()