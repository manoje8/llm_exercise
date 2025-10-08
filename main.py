# Web Scraping + Brochure Automation

from week_1.brochure import get_all_details
from week_1.web_scraping import Website

def main():
    user_input = input("Enter the website URL you want to summarize: ").strip()

    # Ensure proper format
    if not user_input.startswith("http"):
        user_input = "https://" + user_input

    try:
        # Summarize website
        website = Website(user_input)
        print("\nWebsite Summary:\n")
        print(website.summarize())

        # Optionally get full brochure
        generate_brochure = input("\nDo you want to generate the company brochure? (y/n): ").strip().lower()
        if generate_brochure == "y":
            print("\n Generating brochure details...\n")
            details = get_all_details(user_input)
            print(details)

            # Optional: save to file
            with open("company_brochure.txt", "w", encoding="utf-8") as f:
                f.write(details)
            print("\n✅ Brochure saved as company_brochure.txt")

    except Exception as e:
        print(f"\n⚠️ Error occurred: {e}")

if __name__ == "__main__":
    main()
