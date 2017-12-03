/**
 * This module exports a translation function that works like gettext. It looks
 * for a global translations dict and tries to translate phrases by looking
 * for the according key and returning the corresponding value from the dict.
 * If a phrase was not found, it will return the unchanged string and complain
 * on the console.
 *
 * @param phrase The phrase for that the translation shall be returned.
 * @returns The translation for the phrase according to the translations if
 *      available or the original phrase if no translation is available.
 */
module.exports = function(phrase) {
    if (translations === undefined) {
        console.log("gettext.js - No translations available!");
        return phrase;
    }   
    if (phrase in translations) {
        return translations[phrase];
    } else {
        console.log("gettext.js - '" + phrase + "' not found in translations!");
        return phrase;
    }   
};
