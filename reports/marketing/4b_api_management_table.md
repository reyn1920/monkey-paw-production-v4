# API Management & Integration Table

*Last updated: 2024-01-15 10:30:00*

> **🎯 Mission**: Keep paid APIs OFF until we can afford them. Focus on FREE and FREEMIUM tiers only.
> **🔍 Auto-Discovery**: New APIs are automatically discovered and added when channels are created.
> **💰 Cost Tracking**: Monitor usage and costs to stay within budget limits.

## Overview
This table tracks all APIs and services used in the project, their cost status, integration status, and access information.

## Legend
- 🟢 **Free**: No cost or free tier available
- 🟡 **Freemium**: Free tier with paid upgrades
- 🔴 **Paid**: Requires payment
- ⚪ **Unknown**: Cost status needs verification
- ✅ **Active**: Currently integrated and working
- ⚠️ **Inactive**: Configured but not active
- ❌ **Missing**: Not configured

---

## AI & Language Models

| Service | Status | Cost | Environment Variable | Signup URL | Login URL | Notes |
|---------|--------|------|---------------------|------------|-----------|-------|
| OpenAI GPT | ⚠️ | 🔴 | `OPENAI_API_KEY` | [OpenAI Platform](https://platform.openai.com/signup) | [OpenAI Login](https://platform.openai.com/login) | Primary AI service |
| Anthropic Claude | ⚠️ | 🔴 | `ANTHROPIC_API_KEY` | [Anthropic Console](https://console.anthropic.com/) | [Anthropic Login](https://console.anthropic.com/) | Alternative AI model |
| Google AI (Gemini) | ⚠️ | 🟡 | `GOOGLE_AI_API_KEY` | [Google AI Studio](https://makersuite.google.com/) | [Google AI Login](https://makersuite.google.com/) | Free tier available |
| Hugging Face | ⚠️ | 🟢 | `HUGGINGFACE_API_KEY` | [Hugging Face](https://huggingface.co/join) | [HF Login](https://huggingface.co/login) | Free inference API |
| Groq | ⚠️ | 🟢 | `GROQ_API_KEY` | [Groq Console](https://console.groq.com/) | [Groq Login](https://console.groq.com/) | Fast inference, free tier |
| Together AI | ⚠️ | 🟡 | `TOGETHER_API_KEY` | [Together AI](https://api.together.xyz/) | [Together Login](https://api.together.xyz/) | Multiple models |
| RouteLL | ⚠️ | ⚪ | `ROUTELLM_API_KEY` | [RouteLL](https://routellm.com/) | [RouteLL Login](https://routellm.com/) | Model routing service |

---

## Social Media Platforms

| Service | Status | Cost | Environment Variable | Signup URL | Login URL | Notes |
|---------|--------|------|---------------------|------------|-----------|-------|
| YouTube Data API | ⚠️ | 🟢 | `YOUTUBE_API_KEY` | [Google Cloud Console](https://console.cloud.google.com/) | [Google Login](https://accounts.google.com/) | Free quota: 10,000 units/day |
| Twitter/X API | ⚠️ | 🟡 | `TWITTER_API_KEY`, `TWITTER_BEARER_TOKEN` | [Twitter Developer](https://developer.twitter.com/) | [Twitter Login](https://twitter.com/login) | Free tier limited |
| TikTok API | ⚠️ | 🟢 | `TIKTOK_CLIENT_ID`, `TIKTOK_CLIENT_SECRET` | [TikTok Developers](https://developers.tiktok.com/) | [TikTok Login](https://www.tiktok.com/login) | Creator API free |
| Facebook/Meta | ⚠️ | 🟢 | `FACEBOOK_ACCESS_TOKEN` | [Meta Developers](https://developers.facebook.com/) | [Facebook Login](https://www.facebook.com/login) | Basic access free |
| Instagram API | ⚠️ | 🟢 | `INSTAGRAM_ACCESS_TOKEN`, `INSTAGRAM_CLIENT_ID` | [Meta Developers](https://developers.facebook.com/) | [Facebook Login](https://www.facebook.com/login) | Part of Meta platform |
| LinkedIn API | ⚠️ | 🟢 | `LI_CLIENT_ID`, `LI_ACCESS_TOKEN` | [LinkedIn Developers](https://developer.linkedin.com/) | [LinkedIn Login](https://www.linkedin.com/login) | Free tier available |
| Pinterest API | ⚠️ | 🟢 | `PINTEREST_ACCESS_TOKEN` | [Pinterest Developers](https://developers.pinterest.com/) | [Pinterest Login](https://www.pinterest.com/login) | Free for creators |
| Reddit API | ⚠️ | 🟢 | `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET` | [Reddit Apps](https://www.reddit.com/prefs/apps) | [Reddit Login](https://www.reddit.com/login) | Free API access |

---

## Email Marketing & Communication

| Service | Status | Cost | Environment Variable | Signup URL | Login URL | Notes |
|---------|--------|------|---------------------|------------|-----------|-------|
| SendGrid | ⚠️ | 🟡 | `SENDGRID_API_KEY` | [SendGrid](https://signup.sendgrid.com/) | [SendGrid Login](https://app.sendgrid.com/login) | Free: 100 emails/day |
| Mailchimp | ⚠️ | 🟡 | `MAILCHIMP_API_KEY` | [Mailchimp](https://mailchimp.com/signup/) | [Mailchimp Login](https://login.mailchimp.com/) | Free: 2,000 contacts |
| ConvertKit | ⚠️ | 🟡 | `CONVERTKIT_API_KEY` | [ConvertKit](https://convertkit.com/) | [ConvertKit Login](https://app.convertkit.com/users/login) | Free: 1,000 subscribers |

---

## Payment Processing

| Service | Status | Cost | Environment Variable | Signup URL | Login URL | Notes |
|---------|--------|------|---------------------|------------|-----------|-------|
| Stripe | ⚠️ | 🟡 | `STRIPE_API_KEY` | [Stripe](https://dashboard.stripe.com/register) | [Stripe Login](https://dashboard.stripe.com/login) | 2.9% + 30¢ per transaction |
| PayPal | ⚠️ | 🟡 | `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET` | [PayPal Developer](https://developer.paypal.com/) | [PayPal Login](https://www.paypal.com/signin) | 2.9% + fixed fee |
| Gumroad | ⚠️ | 🟡 | `GUMROAD_ACCESS_TOKEN` | [Gumroad](https://gumroad.com/signup) | [Gumroad Login](https://gumroad.com/login) | 3.5% + 30¢ per sale |

---

## Affiliate Marketing Networks

| Service | Status | Cost | Environment Variable | Signup URL | Login URL | Notes |
|---------|--------|------|---------------------|------------|-----------|-------|
| Amazon Associates | ⚠️ | 🟢 | `AMAZON_ASSOCIATE_ID`, `AMAZON_ACCESS_KEY` | [Amazon Associates](https://affiliate-program.amazon.com/) | [Amazon Login](https://affiliate-program.amazon.com/login) | Free to join, 1-10% commission |
| ShareASale | ⚠️ | 🟢 | `SHAREASALE_API_KEY` | [ShareASale](https://www.shareasale.com/shareasale.cfm?call=signup) | [ShareASale Login](https://www.shareasale.com/a-login.cfm) | Free to join |
| Commission Junction | ⚠️ | 🟢 | `COMMISSION_JUNCTION_API_KEY` | [CJ Affiliate](https://www.cj.com/advertiser) | [CJ Login](https://members.cj.com/) | Free to join |
| ClickBank | ❌ | 🟢 | `CLICKBANK_API_KEY` | [ClickBank](https://accounts.clickbank.com/signup/) | [ClickBank Login](https://accounts.clickbank.com/) | Free to join |

---

## E-commerce & Print-on-Demand

| Service | Status | Cost | Environment Variable | Signup URL | Login URL | Notes |
|---------|--------|------|---------------------|------------|-----------|-------|
| Printful | ⚠️ | 🟡 | `PRINTFUL_API_KEY` | [Printful](https://www.printful.com/register) | [Printful Login](https://www.printful.com/dashboard) | Free integration, product costs |
| Teespring/Spring | ⚠️ | 🟡 | `TEESPRING_API_KEY` | [Spring](https://spring.com/) | [Spring Login](https://spring.com/login) | Free to create, revenue share |
| Etsy | ⚠️ | 🟡 | `ETSY_API_KEY`, `ETSY_ACCESS_TOKEN` | [Etsy Developers](https://www.etsy.com/developers/) | [Etsy Login](https://www.etsy.com/signin) | Free API, listing fees |
| Shopify | ❌ | 🔴 | `SHOPIFY_API_KEY` | [Shopify Partners](https://partners.shopify.com/) | [Shopify Login](https://accounts.shopify.com/login) | Monthly subscription |

---

## Content & Media APIs

| Service | Status | Cost | Environment Variable | Signup URL | Login URL | Notes |
|---------|--------|------|---------------------|------------|-----------|-------|
| Pexels | ⚠️ | 🟢 | `PEXELS_API_KEY` | [Pexels API](https://www.pexels.com/api/) | [Pexels Login](https://www.pexels.com/login/) | Free stock photos |
| Pixabay | ⚠️ | 🟢 | `PIXABAY_API_KEY` | [Pixabay API](https://pixabay.com/api/docs/) | [Pixabay Login](https://pixabay.com/accounts/login/) | Free stock images |
| Stability AI | ⚠️ | 🟡 | `STABILITY_API_KEY` | [Stability AI](https://platform.stability.ai/) | [Stability Login](https://platform.stability.ai/) | Image generation |
| ElevenLabs | ⚠️ | 🟡 | `ELEVENLABS_API_KEY` | [ElevenLabs](https://elevenlabs.io/) | [ElevenLabs Login](https://elevenlabs.io/sign-in) | Voice synthesis |
| HeyGen | ⚠️ | 🔴 | `HEYGEN_API_KEY` | [HeyGen](https://www.heygen.com/) | [HeyGen Login](https://app.heygen.com/login) | AI video generation |
| D-ID | ⚠️ | 🔴 | `DID_API_KEY` | [D-ID](https://www.d-id.com/) | [D-ID Login](https://studio.d-id.com/) | AI video avatars |
| Synthesia | ⚠️ | 🔴 | `SYNTHESIA_API_KEY` | [Synthesia](https://www.synthesia.io/) | [Synthesia Login](https://app.synthesia.io/) | AI video creation |
| Medium | ⚠️ | 🟢 | `MEDIUM_ACCESS_TOKEN` | [Medium Developers](https://github.com/Medium/medium-api-docs) | [Medium Login](https://medium.com/m/signin) | Free publishing API |

---

## News & Information APIs

| Service | Status | Cost | Environment Variable | Signup URL | Login URL | Notes |
|---------|--------|------|---------------------|------------|-----------|-------|
| NewsAPI | ⚠️ | 🟡 | `NEWSAPI_KEY` | [NewsAPI](https://newsapi.org/register) | [NewsAPI Login](https://newsapi.org/login) | Free: 1,000 requests/day |
| Guardian API | ⚠️ | 🟢 | `GUARDIAN_API_KEY` | [Guardian Open Platform](https://open-platform.theguardian.com/) | [Guardian Login](https://profile.theguardian.com/signin) | Free tier available |
| NY Times API | ⚠️ | 🟢 | `NYTIMES_API_KEY` | [NY Times Developer](https://developer.nytimes.com/) | [NYT Login](https://myaccount.nytimes.com/auth/login) | Free tier: 1,000 calls/day |

---

## Weather & Location APIs

| Service | Status | Cost | Environment Variable | Signup URL | Login URL | Notes |
|---------|--------|------|---------------------|------------|-----------|-------|
| OpenWeatherMap | ⚠️ | 🟡 | `OPENWEATHERMAP_API_KEY` | [OpenWeatherMap](https://openweathermap.org/api) | [OWM Login](https://home.openweathermap.org/users/sign_in) | Free: 1,000 calls/day |
| OpenCage Geocoding | ⚠️ | 🟡 | `OPENCAGE_API_KEY` | [OpenCage](https://opencagedata.com/api) | [OpenCage Login](https://opencagedata.com/dashboard) | Free: 2,500 requests/day |

---

## Pet & Fun APIs

| Service | Status | Cost | Environment Variable | Signup URL | Login URL | Notes |
|---------|--------|------|---------------------|------------|-----------|-------|
| The Cat API | ⚠️ | 🟡 | `THECATAPI_KEY` | [The Cat API](https://thecatapi.com/) | [Cat API Login](https://thecatapi.com/signup) | Free tier available |
| The Dog API | ⚠️ | 🟡 | `THEDOGAPI_KEY` | [The Dog API](https://thedogapi.com/) | [Dog API Login](https://thedogapi.com/signup) | Free tier available |
| Petfinder | ⚠️ | 🟢 | `PETFINDER_API_KEY` | [Petfinder Developers](https://www.petfinder.com/developers/) | [Petfinder Login](https://www.petfinder.com/user/login/) | Free API |

---

## Analytics & SEO

| Service | Status | Cost | Environment Variable | Signup URL | Login URL | Notes |
|---------|--------|------|---------------------|------------|-----------|-------|
| Google Analytics | ⚠️ | 🟢 | `GOOGLE_ANALYTICS_CREDENTIALS` | [Google Analytics](https://analytics.google.com/) | [Google Login](https://accounts.google.com/) | Free web analytics |
| Google Search Console | ⚠️ | 🟢 | `GOOGLE_SEARCH_CONSOLE_CREDENTIALS` | [Search Console](https://search.google.com/search-console) | [Google Login](https://accounts.google.com/) | Free SEO tools |

---

## Cost Management Strategy

### Free Services to Prioritize
1. **YouTube Data API** - Essential for content creators
2. **Hugging Face** - Free AI inference
3. **Groq** - Fast, free AI inference
4. **Reddit API** - Free social media access
5. **Pexels/Pixabay** - Free stock images
6. **Guardian/NY Times APIs** - Free news content

### Freemium Services (Use Free Tiers)
1. **SendGrid** - 100 emails/day free
2. **Mailchimp** - 2,000 contacts free
3. **NewsAPI** - 1,000 requests/day free
4. **OpenWeatherMap** - 1,000 calls/day free

### Paid Services to Defer
1. **OpenAI GPT** - Use Groq/Hugging Face instead
2. **HeyGen/D-ID/Synthesia** - Expensive video generation
3. **Shopify** - Monthly subscription fees

---

## Action Items

### Immediate (Free Services)
- [ ] Set up YouTube Data API
- [ ] Configure Groq API for AI inference
- [ ] Set up Hugging Face API
- [ ] Configure Reddit API
- [ ] Set up Pexels API for images

### Phase 2 (Freemium - Free Tiers)
- [ ] Set up SendGrid (100 emails/day)
- [ ] Configure Mailchimp (2,000 contacts)
- [ ] Set up NewsAPI (1,000 requests/day)
- [ ] Configure OpenWeatherMap (1,000 calls/day)

### Phase 3 (When Revenue Allows)
- [ ] Upgrade to OpenAI GPT
- [ ] Add premium video generation services
- [ ] Upgrade email marketing limits

---

## Environment Variables Checklist

### Currently Missing (High Priority)
```bash
# Free APIs to set up immediately
YOUTUBE_API_KEY=
GROQ_API_KEY=
HUGGINGFACE_API_KEY=
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
PEXELS_API_KEY=
PIXABY_API_KEY=

# Freemium APIs (free tiers)
SENDGRID_API_KEY=
MAILCHIMP_API_KEY=
NEWSAPI_KEY=
OPENWEATHERMAP_API_KEY=
```

### Paid APIs (Defer Until Profitable)
```bash
# Expensive APIs to avoid for now
OPENAI_API_KEY=
HEYGEN_API_KEY=
DID_API_KEY=
SYNTHESIA_API_KEY=
STRIPE_API_KEY=
```

---

*Last Updated: $(date)*
*Total Free APIs Available: 15+*
*Total Freemium APIs: 10+*
*Estimated Monthly Cost (Free Tier Only): $0*
