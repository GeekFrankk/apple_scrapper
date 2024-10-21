const { CrawlingAPI } = require('crawlbase'),
  cheerio = require('cheerio'),
  fs = require('fs'),
  path = require('path');

const crawlbaseToken = 'tZ0jkO_lHx4geybqVi-I_A';
const api = new CrawlingAPI({ token: crawlbaseToken });

// Array of App Store URLs to be scraped
const appStoreUrls = [
  'https://apps.apple.com/us/app/klinio-health-weight-loss/id1511958049',
  'https://apps.apple.com/us/app/curable/id1325784379',
  ' ',
  '',
  '',
  '',
  '',
  '',
  '',
  '',
];

// Output folder for the JSON and HTML files
const outputFolder = path.join(__dirname, './json&html_files');

// Function to scrape a single app URL
function scrapeApp(url) {
  return api.get(url).then((response) => {
    if (response.statusCode === 200) {
      const appId = url.split('/id')[1]; // Extract app ID for file naming

      // Save the HTML to a file
      const htmlFilePath = path.join(outputFolder, `${appId}.html`);
      fs.writeFileSync(htmlFilePath, response.body);
      console.log(`HTML saved to ${appId}.html in json&html_files folder`);

      // Load the HTML into Cheerio for scraping
      const $ = cheerio.load(response.body);
      const select = (selector) => $(selector);

      // Extract necessary data using selectors
      const imageUrl = select('.we-artwork__image').attr('src');

      const [title, subtitle, seller, starsText, price, appDescription] = [
        '.product-header__title',
        '.product-header__subtitle',
        '.product-header__identity a',
        '.we-rating-count.star-rating__count',
        '.app-header__list__item--price',
        '.section__description .we-truncate',
      ].map((selector) => select(selector).text().replace(/\n\n/g, '\n').replace(/\s+/g, ' ').trim());

      const [stars, rating] = starsText.split(' • ');

      const reviews = $('.we-customer-review')
        .map(function () {
          const user = select(this).find('.we-customer-review__user').text().trim();
          const date = select(this).find('.we-customer-review__date').text().trim();
          const title = select(this).find('.we-customer-review__title').text().trim();
          const review = select(this).find('.we-customer-review__body').text().replace(/\n\n/g, '\n').replace(/\s+/g, ' ').trim();

          return { user, date, title, review };
        })
        .get();

      const compatibility = select(
        '.information-list__item.l-column.small-12.medium-6.large-4.small-valign-top:has(dt) dl.information-list__item__definition__item dt.information-list__item__definition__item__term',
      )
        .map(function () {
          return select(this).text().trim();
        })
        .get();

      const [size, category, ageRating, languages] = [
        ".information-list__item__term:contains('Size') + dd",
        ".information-list__item__term:contains('Category') + dd a",
        ".information-list__item__term:contains('Age Rating') + dd",
        ".information-list__item__term:contains('Languages') + dd p",
      ].map((selector) => select(selector).text().trim());

      // Create app info object
      const appInfo = {
        imageUrl,
        title,
        subtitle,
        seller,
        stars,
        rating,
        price,
        appDescription,
        reviews,
        compatibility,
        size,
        category,
        ageRating,
        languages,
      };

      // Save the extracted data to a JSON file
      const jsonFilePath = path.join(outputFolder, `${appId}.json`);
      const jsonResult = JSON.stringify(appInfo, null, 2);
      fs.writeFileSync(jsonFilePath, jsonResult, 'utf-8');
      console.log(`Scraped data saved to ${appId}.json in json&html_files folder`);
    }
  }).catch((error) => {
    console.error(`Error during crawling of ${url}:`, error);
  });
}

// Loop through each URL and scrape the data
async function scrapeAllApps() {
  for (const url of appStoreUrls) {
    await scrapeApp(url); // Scrape each app sequentially
  }
}

// Start scraping process
scrapeAllApps();
