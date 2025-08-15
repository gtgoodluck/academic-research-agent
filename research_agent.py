# """
# Academic Research Agent
# Uses Ollama Llama + Playwright to research academic papers
# """

# import time
# import datetime
# from typing import Dict, Any, List
# from langchain.agents import AgentExecutor, create_react_agent
# from langchain.tools import Tool
# from langchain_community.llms import Ollama
# from langchain.prompts import PromptTemplate

# class AcademicResearchAgent:
#     """
#     AI Agent specialized in academic research
#     Can search Google Scholar, find papers, and summarize content
#     """
    
#     def __init__(self):
#         # Initialize Ollama Llama (FREE, LOCAL)
#         self.llm = Ollama(
#             model="llama3.2",
#             temperature=0.1
#         )
        
#         # Set up research tools
#         self.tools = self._setup_research_tools()
#         self.agent = self._create_research_agent()
#         self.agent_executor = AgentExecutor(
#             agent=self.agent,
#             tools=self.tools,
#             verbose=True,
#             max_iterations=3,
#             handle_parsing_errors=True
#         )
    
#     def _setup_research_tools(self) -> List[Tool]:
#         """Set up academic research tools"""
#         return [
#             Tool(
#                 name="scholar_search",
#                 description="Search Google Scholar for papers by author name. Input should be author name like 'Geoffrey Hinton' or 'Yann LeCun'",
#                 func=self._search_google_scholar
#             ),
#             Tool(
#                 name="paper_analyzer",
#                 description="Analyze and summarize a research paper from its URL. Input should be the paper URL.",
#                 func=self._analyze_paper
#             )
#         ]
    
#     def _create_research_agent(self):
#         """Create research-focused agent"""
#         prompt_template = """
#         You are an academic research assistant AI. Help users research papers and authors.

#         Available tools:
#         {tools}

#         Tool names: {tool_names}

#         Use this format:
#         Question: the research question
#         Thought: think about the best research approach
#         Action: the action to take (use one of: {tool_names})
#         Action Input: the input to the action
#         Observation: the result of the action
#         ... (repeat as needed)
#         Thought: I have found the papers, now I should present them to the user
#         Final Answer: List all papers found and ask user which one to analyze

#         Question: {input}
#         Thought: {agent_scratchpad}
#         """
        
#         prompt = PromptTemplate(
#             template=prompt_template,
#             input_variables=["input", "tools", "tool_names", "agent_scratchpad"]
#         )
        
#         return create_react_agent(self.llm, self.tools, prompt)
    
#     def research_papers_interactive(self, author_name: str) -> Dict[str, Any]:
#         """Interactive research method that shows papers first, then analyzes chosen one"""
#         start_time = time.time()
        
#         try:
#             print(f"\n🎓 Academic Research Agent processing: {author_name}")
            
#             # Step 1: Search for papers
#             print(f"\n📚 **Step 1: Finding papers by {author_name}**")
#             papers_result = self._search_google_scholar(author_name)
            
#             # Parse papers and extract URLs
#             paper_urls = []
#             paper_titles = []
            
#             if "🔗" in papers_result:
#                 lines = papers_result.split('\n')
#                 current_title = None
                
#                 for line in lines:
#                     line = line.strip()
#                     if line and line[0].isdigit() and '. ' in line:
#                         # This is a title line
#                         current_title = line.split('. ', 1)[1] if '. ' in line else line
#                         paper_titles.append(current_title)
#                     elif line.startswith('🔗 '):
#                         # This is a URL line
#                         url = line.replace('🔗 ', '').strip()
#                         paper_urls.append(url)
            
#             # Display papers
#             print(papers_result)
            
#             # If no papers found, return early
#             if not paper_titles:
#                 return {
#                     "findings": f"No papers found for {author_name}",
#                     "research_time": time.time() - start_time,
#                     "status": "no_papers_found"
#                 }
            
#             # Step 2: Interactive paper selection
#             print(f"\n📋 **Step 2: Choose a paper to analyze in detail**")
#             print(f"Found {len(paper_titles)} paper(s). Which would you like me to analyze?")
            
#             # Show numbered options
#             for i, title in enumerate(paper_titles, 1):
#                 print(f"{i}. {title}")
            
#             print(f"{len(paper_titles) + 1}. Skip detailed analysis")
            
#             # Get user choice
#             while True:
#                 try:
#                     choice = input(f"\nEnter your choice (1-{len(paper_titles) + 1}): ").strip()
                    
#                     if not choice:
#                         continue
                        
#                     choice_num = int(choice)
                    
#                     if choice_num == len(paper_titles) + 1:
#                         # Skip analysis
#                         return {
#                             "findings": f"Papers by {author_name}:\n\n{papers_result}\n\n📋 Analysis skipped by user choice.",
#                             "research_time": time.time() - start_time,
#                             "status": "analysis_skipped"
#                         }
#                     elif 1 <= choice_num <= len(paper_titles):
#                         selected_title = paper_titles[choice_num - 1]
#                         selected_url = paper_urls[choice_num - 1] if choice_num - 1 < len(paper_urls) else None
#                         break
#                     else:
#                         print(f"❌ Please enter a number between 1 and {len(paper_titles) + 1}")
                        
#                 except ValueError:
#                     print("❌ Please enter a valid number")
#                 except KeyboardInterrupt:
#                     return {
#                         "findings": f"Research interrupted by user",
#                         "research_time": time.time() - start_time,
#                         "status": "interrupted"
#                     }
            
#             # Step 3: Analyze selected paper
#             print(f"\n📄 **Step 3: Analyzing selected paper**")
#             print(f"🎯 **Selected:** {selected_title}")
            
#             if selected_url:
#                 print(f"🔗 **URL:** {selected_url}")
#                 analysis_result = self._analyze_paper(selected_url)
#             else:
#                 analysis_result = f"❌ No accessible URL found for this paper. Analysis not possible."
            
#             # Step 4: Compile final results
#             final_results = f"""📚 **Research Summary for {author_name}:**

# {papers_result}

# 📄 **Detailed Analysis of Selected Paper:**
# **Title:** {selected_title}

# {analysis_result}"""
            
#             elapsed = time.time() - start_time
#             return {
#                 "findings": final_results,
#                 "research_time": elapsed,
#                 "status": "research_complete"
#             }
            
#         except Exception as e:
#             return {
#                 "findings": f"Research error: {str(e)}",
#                 "research_time": time.time() - start_time,
#                 "status": "research_failed"
#             }
    
#     def research(self, query: str) -> Dict[str, Any]:
#         """Main research method"""
#         start_time = time.time()
        
#         try:
#             print(f"\n🎓 Academic Research Agent processing: {query}")
#             result = self.agent_executor.invoke({"input": query})
            
#             elapsed = time.time() - start_time
#             return {
#                 "findings": result["output"],
#                 "research_time": elapsed,
#                 "status": "research_complete"
#             }
            
#         except Exception as e:
#             return {
#                 "findings": f"Research error: {str(e)}",
#                 "research_time": time.time() - start_time,
#                 "status": "research_failed"
#             }
    
#     def _search_google_scholar(self, author_name: str) -> str:
#         """Search Google Scholar for author's papers"""
#         print(f"📚 Searching Google Scholar for: {author_name}")
        
#         try:
#             from playwright.sync_api import sync_playwright
            
#             with sync_playwright() as p:
#                 browser = p.chromium.launch(headless=True)
#                 page = browser.new_page()
                
#                 # More precise Google Scholar search with author quotes
#                 search_url = f'https://scholar.google.com/scholar?q=author:"{author_name.replace(" ", "+")}"&hl=en'
#                 print(f"🔍 Search URL: {search_url}")
#                 page.goto(search_url, wait_until="networkidle", timeout=15000)
                
#                 # Wait for results
#                 try:
#                     page.wait_for_selector('.gs_rt', timeout=10000)
#                 except:
#                     print("⚠️ No results found or page didn't load properly")
#                     browser.close()
#                     return f"No search results found for {author_name} on Google Scholar"
                
#                 # Extract paper information with better filtering
#                 results = page.query_selector_all('.gs_r')[:10]  # Get more results to filter
#                 print(f"🔍 Found {len(results)} raw results to process")
                
#                 if results:
#                     author_results = f"📖 Papers by {author_name}:\n\n"
#                     paper_links = []
#                     valid_papers = 0
                    
#                     for i, result in enumerate(results):
#                         try:
#                             # Get title and link from result
#                             title_element = result.query_selector('.gs_rt a')
#                             if not title_element:
#                                 print(f"⚠️ Result {i+1}: No title element found")
#                                 continue
                                
#                             title = title_element.inner_text().strip()
#                             url = title_element.get_attribute('href')
                            
#                             print(f"📄 Result {i+1}: {title[:60]}...")
                            
#                             # Get author information to verify relevance
#                             author_element = result.query_selector('.gs_a')
#                             author_text = author_element.inner_text() if author_element else ""
                            
#                             print(f"👥 Authors found: {author_text[:100]}...")
                            
#                             # More lenient filtering: check if any part of the searched name appears
#                             author_name_parts = author_name.lower().split()
#                             author_text_lower = author_text.lower()
                            
#                             # Check different name combinations
#                             name_variations = [
#                                 author_name.lower(),  # Full name
#                                 " ".join(author_name_parts[-2:]) if len(author_name_parts) >= 2 else author_name.lower(),  # Last two parts
#                                 author_name_parts[-1] if author_name_parts else "",  # Last name only
#                             ]
                            
#                             # Add initials + last name for academic papers (e.g., "T Goodluck Constance")
#                             if len(author_name_parts) >= 2:
#                                 initials_last = f"{author_name_parts[0][0].lower()} {' '.join(author_name_parts[1:]).lower()}"
#                                 name_variations.append(initials_last)
                            
#                             # Check if any variation matches
#                             is_relevant = any(variation in author_text_lower for variation in name_variations if variation)
                            
#                             # print(f"🔍 Checking variations: {name_variations}")
#                             # print(f"✅ Relevant: {is_relevant}")
                            
#                             # Additional check: avoid obviously unrelated papers
#                             unrelated_keywords = ['user profiles', 'profiles for author', 'author:', 'citations?view_op']
#                             is_unrelated = any(keyword in title.lower() for keyword in unrelated_keywords)
                            
#                             if is_relevant and not is_unrelated and valid_papers < 8:  # Allow more papers
#                                 valid_papers += 1
#                                 author_results += f"{valid_papers}. {title}\n"
                                
#                                 # Show authors if available
#                                 if author_text:
#                                     # Clean up author text (remove extra info)
#                                     clean_authors = author_text.split('-')[0].split('…')[0].strip()
#                                     author_results += f"   👥 Authors: {clean_authors}\n"
                                
#                                 if url and not url.startswith('https://scholar.google.com/citations'):
#                                     author_results += f"   🔗 {url}\n"
#                                     paper_links.append(url)
                                
#                                 author_results += "\n"
#                             else:
#                                 print(f"❌ Filtered out: relevant={is_relevant}, unrelated={is_unrelated}")
                                
#                         except Exception as e:
#                             print(f"❌ Error processing result {i+1}: {e}")
#                             continue
                    
#                     if valid_papers > 0:
#                         author_results += f"📋 Found {valid_papers} relevant papers"
#                         if paper_links:
#                             author_results += f" with {len(paper_links)} accessible for analysis."
#                             # Store first paper link for potential analysis
#                             self._latest_paper_url = paper_links[0]
#                         else:
#                             author_results += "."
                        
#                         browser.close()
#                         return author_results
#                     else:
#                         print("❌ No relevant papers found after filtering")
#                         browser.close()
                        
#                         # Fallback: try a broader search
#                         print("🔄 Trying broader search...")
#                         return self._search_google_scholar_broad(author_name)
                
#                 browser.close()
#                 return f"No search results found for {author_name} on Google Scholar"
                
#         except ImportError:
#             return "Playwright not installed. Please install: pip install playwright && playwright install chromium"
#         except Exception as e:
#             print(f"❌ Scholar search error: {e}")
#             return f"Scholar search failed: {str(e)}. This might be due to Google Scholar rate limiting or network issues."
    
#     def _search_google_scholar_broad(self, author_name: str) -> str:
#         """Fallback broader search for author's papers"""
#         print(f"📚 Trying broader search for: {author_name}")
        
#         try:
#             from playwright.sync_api import sync_playwright
            
#             with sync_playwright() as p:
#                 browser = p.chromium.launch(headless=True)
#                 page = browser.new_page()
                
#                 # Broader search without strict author quotes
#                 search_url = f'https://scholar.google.com/scholar?q={author_name.replace(" ", "+")}&hl=en'
#                 print(f"🔍 Broad search URL: {search_url}")
#                 page.goto(search_url, wait_until="networkidle", timeout=15000)
                
#                 # Wait for results
#                 page.wait_for_selector('.gs_rt', timeout=10000)
                
#                 # Extract first few results with minimal filtering
#                 results = page.query_selector_all('.gs_r')[:5]
                
#                 if results:
#                     author_results = f"📖 Papers related to {author_name}:\n\n"
#                     paper_links = []
                    
#                     for i, result in enumerate(results, 1):
#                         try:
#                             title_element = result.query_selector('.gs_rt a')
#                             if title_element:
#                                 title = title_element.inner_text().strip()
#                                 url = title_element.get_attribute('href')
                                
#                                 # Get author info
#                                 author_element = result.query_selector('.gs_a')
#                                 author_text = author_element.inner_text() if author_element else ""
                                
#                                 # Basic filtering - just remove obvious non-papers
#                                 unrelated_keywords = ['user profiles', 'profiles for author']
#                                 is_unrelated = any(keyword in title.lower() for keyword in unrelated_keywords)
                                
#                                 if not is_unrelated:
#                                     author_results += f"{i}. {title}\n"
                                    
#                                     if author_text:
#                                         clean_authors = author_text.split('-')[0].split('…')[0].strip()
#                                         author_results += f"   👥 Authors: {clean_authors}\n"
                                    
#                                     if url and not url.startswith('https://scholar.google.com/citations'):
#                                         author_results += f"   🔗 {url}\n"
#                                         paper_links.append(url)
                                    
#                                     author_results += "\n"
#                         except:
#                             continue
                    
#                     author_results += f"📋 Found {len(paper_links)} papers (broader search)"
#                     if paper_links:
#                         self._latest_paper_url = paper_links[0]
                    
#                     browser.close()
#                     return author_results
                
#                 browser.close()
#                 return f"No papers found for {author_name} even with broader search"
                
#         except Exception as e:
#             print(f"❌ Broad search failed: {e}")
#             return f"Both precise and broad searches failed for {author_name}"
    
#     def _analyze_paper(self, paper_url: str) -> str:
#         """Analyze and summarize a research paper"""
#         print(f"📄 Analyzing paper: {paper_url[:50]}...")
        
#         try:
#             from playwright.sync_api import sync_playwright
            
#             with sync_playwright() as p:
#                 browser = p.chromium.launch(headless=True)
#                 page = browser.new_page()
                
#                 # Navigate to paper
#                 page.goto(paper_url, wait_until="networkidle", timeout=15000)
#                 time.sleep(3)  # Let page fully load
                
#                 # Try to extract paper content
#                 content = self._extract_paper_content(page)
                
#                 browser.close()
                
#                 if content:
#                     # Use Ollama to summarize
#                     summary_prompt = f"""
#                     Analyze this research paper content and provide a structured summary:
                    
#                     {content}
                    
#                     Please provide:
#                     1. Main research question/problem
#                     2. Key methodology or approach
#                     3. Major findings/contributions
#                     4. Significance to the field
                    
#                     Keep the summary concise but informative.
#                     """
                    
#                     summary = self.llm.invoke(summary_prompt)
                    
#                     return f"""📋 **Paper Analysis:**

# {summary}

# 🔗 **Source:** {paper_url}
# ⏰ **Analyzed:** {datetime.datetime.now().strftime('%H:%M:%S')}"""
                
#                 return f"Could not extract content from: {paper_url}"
                
#         except Exception as e:
#             return f"Paper analysis failed: {str(e)}"
    
#     def _extract_paper_content(self, page) -> str:
#         """Extract text content from paper page"""
#         try:
#             # Try different selectors for paper content
#             content_selectors = [
#                 '.ltx_abstract',  # arXiv abstract
#                 '#abstract',      # Many journal abstracts
#                 '.abstract',      # Generic abstract
#                 'article p',      # Article paragraphs
#                 '.content p',     # Content paragraphs
#                 'p'               # Any paragraphs
#             ]
            
#             extracted_content = ""
            
#             for selector in content_selectors:
#                 try:
#                     elements = page.query_selector_all(selector)
#                     if elements and len(elements) > 0:
#                         for element in elements[:5]:  # First 5 relevant elements
#                             text = element.inner_text().strip()
#                             if len(text) > 50:  # Only substantial text
#                                 extracted_content += f"{text}\n\n"
                        
#                         if len(extracted_content) > 200:  # Enough content found
#                             break
#                 except:
#                     continue
            
#             return extracted_content[:1500] if extracted_content else ""  # Limit length
            
#         except Exception as e:
#             print(f"Content extraction error: {e}")
#             return ""

# def demo_research_agent():
#     """Demonstrate the academic research agent"""
    
#     print("🎓 ACADEMIC RESEARCH AGENT DEMO")
#     print("=" * 60)
#     print("🦙 Using Ollama Llama + Playwright for Academic Research")
#     print("=" * 60)
    
#     # Check setup
#     try:
#         agent = AcademicResearchAgent()
#         print("✅ Research agent initialized successfully!")
#     except Exception as e:
#         print(f"❌ Setup error: {e}")
#         return
    
#     # Interactive researcher selection
#     print("\n🔬 **Interactive Academic Research Demo**")
#     print("💡 **Popular AI Researchers you could try:**")
#     print("   • Geoffrey Hinton (Deep Learning pioneer)")
#     print("   • Yann LeCun (CNN inventor, Meta AI)")
#     print("   • Fei-Fei Li (Computer Vision expert)")
#     print("   • Andrew Ng (Online education, former Stanford)")
#     print("   • Yoshua Bengio (Neural Networks, Turing Award)")
#     print("   • Demis Hassabis (DeepMind founder)")
#     print("   • Or any researcher you're curious about!")
    
#     # Get researcher name from user
#     while True:
#         researcher_name = input(f"\n👨‍🔬 Enter researcher name to search: ").strip()
        
#         if not researcher_name:
#             print("❌ Please enter a researcher name!")
#             continue
        
#         if researcher_name.lower() in ['quit', 'exit', 'q']:
#             print("👋 Exiting demo. Goodbye!")
#             return
        
#         # Confirm the search
#         confirm = input(f"🔍 Search for papers by '{researcher_name}'? (y/n): ").lower()
#         if confirm in ['y', 'yes', '']:
#             break
#         elif confirm in ['n', 'no']:
#             print("Let's try a different researcher...")
#             continue
    
#     print(f"\n{'='*60}")
#     print(f"🔍 **Researching:** {researcher_name}")
#     print(f"{'='*60}")
    
#     # Perform interactive research
#     print(f"🤖 Starting interactive research process...")
#     results = agent.research_papers_interactive(researcher_name)
    
#     print(f"\n{'='*60}")
#     print(f"📋 **Final Research Summary:**")
#     print(f"{'='*60}")
#     print(results["findings"])
#     print(f"\n⏱️ **Total research time:** {results['research_time']:.2f} seconds")
#     print(f"📊 **Status:** {results['status']}")
    
#     # Ask if they want to try another researcher
#     print(f"\n🎯 **Want to research another academic?**")
#     while True:
#         another = input("Try another researcher? (y/n): ").lower()
#         if another in ['y', 'yes']:
#             print(f"\n{'-'*40}")
#             demo_research_agent()  # Recursive call for another search
#             break
#         elif another in ['n', 'no']:
#             print("👋 Thank you for using the Academic Research Agent!")
#             break
#         else:
#             print("Please enter 'y' for yes or 'n' for no")

# def interactive_research_mode():
#     """Continuous interactive research mode"""
#     print("🔄 INTERACTIVE RESEARCH MODE")
#     print("=" * 50)
#     print("💡 Research multiple academics in one session!")
#     print("=" * 50)
    
#     # Initialize agent
#     try:
#         agent = AcademicResearchAgent()
#         print("✅ Interactive mode ready!")
#     except Exception as e:
#         print(f"❌ Setup error: {e}")
#         return
    
#     while True:
#         print(f"\n🔬 **Who would you like to research?**")
#         researcher_name = input(f"👨‍🔬 Enter researcher name (or 'quit' to exit): ").strip()
        
#         if not researcher_name:
#             print("❌ Please enter a researcher name!")
#             continue
        
#         if researcher_name.lower() in ['quit', 'exit', 'q', 'done']:
#             print("👋 Exiting interactive mode. Goodbye!")
#             break
        
#         print(f"\n🔍 **Researching:** {researcher_name}")
#         print(f"{'='*50}")
        
#         # Perform research
#         results = agent.research_papers_interactive(researcher_name)
        
#         print(f"\n📋 **Research Complete:**")
#         print(results["findings"])
#         print(f"\n⏱️ **Research time:** {results['research_time']:.2f} seconds")
        
#         print(f"\n{'-'*50}")

# def lecture_demo_mode():
#     """Optimized mode for live lecture demonstrations"""
    
#     print("🎓 LECTURE DEMO MODE")
#     print("=" * 50)
#     print("🎯 **Perfect for Live Demonstrations**")
#     print("💫 **Interactive Demo Flow:**")
#     print("   1. Ask audience for researcher suggestions")
#     print("   2. Show all papers by that researcher")
#     print("   3. Let audience vote on which paper to analyze")
#     print("   4. AI analyzes and presents findings")
#     print("   5. Discuss results with audience")
#     print("=" * 50)
    
#     # Initialize agent
#     try:
#         agent = AcademicResearchAgent()
#         print("✅ Demo agent ready for lecture!")
#     except Exception as e:
#         print(f"❌ Setup error: {e}")
#         return
    
#     # Suggested researchers for quick demo
#     print(f"\n💡 **Quick Demo Suggestions:**")
#     suggestions = [
#         "Geoffrey Hinton", "Yann LeCun", "Fei-Fei Li", 
#         "Andrew Ng", "Yoshua Bengio", "Demis Hassabis"
#     ]
    
#     for i, name in enumerate(suggestions, 1):
#         print(f"   {i}. {name}")
    
#     print(f"\n🎤 **For Live Demo:**")
    
#     while True:
#         print(f"\n👥 Ask your audience: 'Which AI researcher should we investigate?'")
#         researcher_name = input(f"🎯 Enter researcher name from audience suggestion: ").strip()
        
#         if not researcher_name:
#             print("⏸️  Waiting for audience suggestion...")
#             continue
        
#         if researcher_name.lower() in ['quit', 'exit', 'done']:
#             print("🎉 Lecture demo complete!")
#             break
        
#         # Quick confirmation for lecture pace
#         print(f"\n📢 **Announcing to audience:** 'Let's research {researcher_name}!'")
#         input("Press Enter when ready to start demo... ")
        
#         print(f"\n🔴 **LIVE DEMO IN PROGRESS**")
#         print(f"🔍 Researching: {researcher_name}")
#         print(f"{'='*50}")
        
#         # Execute interactive research for live audience
#         print(f"🎤 **[Tell audience: 'Watch the AI find and analyze real research papers!']**")
#         results = agent.research_papers_interactive(researcher_name)
        
#         # Present results to audience
#         print(f"\n📋 **LIVE RESULTS FOR AUDIENCE:**")
#         print("🎤 **[Present these findings to your audience]**")
#         print("=" * 50)
#         print(results["findings"])
#         print("=" * 50)
#         print(f"⏱️ **Demo completed in:** {results['research_time']:.2f} seconds")
        
#         # Audience interaction prompt
#         print(f"\n🎤 **Audience Discussion Points:**")
#         print(f"   • 'What do you think about these research findings?'")
#         print(f"   • 'How could AI help researchers like this?'")
#         print(f"   • 'Did the AI correctly identify relevant papers?'")
#         print(f"   • 'Should we investigate another researcher?'")
        
#         # Continue or finish
#         continue_demo = input(f"\n🔄 Continue with another researcher? (y/n): ").lower()
#         if continue_demo not in ['y', 'yes']:
#             print("🎉 Lecture demo session complete!")
#             break

# if __name__ == "__main__":
#     print("🎓 **ACADEMIC RESEARCH AGENT - CLEAN VERSION**")
#     print("Choose your mode:")
#     print("1. 🎯 Single Research Demo")
#     print("2. 🔄 Interactive Research Mode") 
#     print("3. 🎤 Lecture Demo Mode")
    
#     while True:
#         choice = input("\nSelect mode (1/2/3): ").strip()
        
#         if choice == "1":
#             demo_research_agent()
#             break
#         elif choice == "2":
#             interactive_research_mode()
#             break
#         elif choice == "3":
#             lecture_demo_mode()
#             break
#         else:
#             print("❌ Please enter 1, 2, or 3")

"""
Academic Research Agent - Multi-Provider Support
Uses LangChain with multiple LLM providers (Ollama, OpenAI, Anthropic) + Playwright
"""

import time
import datetime
import os
from typing import Dict, Any, List, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not installed. API keys must be set as environment variables.")

class AcademicResearchAgent:
    """
    AI Agent specialized in academic research
    Can search Google Scholar, find papers, and summarize content
    Supports multiple LLM providers: Ollama, OpenAI, Anthropic
    """
    
    def __init__(self, provider: str = "ollama", model: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize the research agent with specified LLM provider
        
        Args:
            provider: LLM provider ("ollama", "openai", "anthropic")
            model: Specific model name (optional, uses defaults)
            api_key: API key for cloud providers (optional, uses env vars)
        """
        self.provider = provider.lower()
        self.llm = self._initialize_llm(provider, model, api_key)
        
        # Set up research tools
        self.tools = self._setup_research_tools()
        self.agent = self._create_research_agent()
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=3,
            handle_parsing_errors=True
        )
        
        print(f"✅ Research agent initialized with {self.provider.upper()} provider")
    
    def _initialize_llm(self, provider: str, model: Optional[str] = None, api_key: Optional[str] = None):
        """Initialize LLM based on provider"""
        provider = provider.lower()
        
        try:
            if provider == "ollama":
                from langchain_community.llms import Ollama
                model_name = model or "llama3.2"
                print(f"🦙 Initializing Ollama with model: {model_name}")
                return Ollama(
                    model=model_name,
                    temperature=0.1
                )
                
            elif provider == "openai":
                from langchain_openai import ChatOpenAI
                model_name = model or "gpt-4"
                openai_key = api_key or os.getenv("OPENAI_API_KEY")
                
                if not openai_key:
                    raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
                
                print(f"🤖 Initializing OpenAI with model: {model_name}")
                return ChatOpenAI(
                    model=model_name,
                    temperature=0.1,
                    openai_api_key=openai_key
                )
                
            elif provider == "anthropic":
                from langchain_anthropic import ChatAnthropic
                model_name = model or "claude-3-sonnet-20240229"
                anthropic_key = api_key or os.getenv("ANTHROPIC_API_KEY")
                
                if not anthropic_key:
                    raise ValueError("Anthropic API key required. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter.")
                
                print(f"🧠 Initializing Anthropic with model: {model_name}")
                return ChatAnthropic(
                    model=model_name,
                    temperature=0.1,
                    anthropic_api_key=anthropic_key
                )
                
            else:
                raise ValueError(f"Unsupported provider: {provider}. Choose from: ollama, openai, anthropic")
                
        except ImportError as e:
            raise ImportError(f"Required package not installed for {provider}. Install with: pip install langchain-{provider}")
        except Exception as e:
            raise Exception(f"Failed to initialize {provider}: {str(e)}")
    
    @classmethod
    def create_ollama_agent(cls, model: str = "llama3.2"):
        """Convenience method to create Ollama agent"""
        return cls(provider="ollama", model=model)
    
    @classmethod
    def create_openai_agent(cls, model: str = "gpt-4", api_key: Optional[str] = None):
        """Convenience method to create OpenAI agent"""
        return cls(provider="openai", model=model, api_key=api_key)
    
    @classmethod
    def create_anthropic_agent(cls, model: str = "claude-3-sonnet-20240229", api_key: Optional[str] = None):
        """Convenience method to create Anthropic agent"""
        return cls(provider="anthropic", model=model, api_key=api_key)
    
    def _setup_research_tools(self) -> List[Tool]:
        """Set up academic research tools"""
        return [
            Tool(
                name="scholar_search",
                description="Search Google Scholar for papers by author name. Input should be author name like 'Geoffrey Hinton' or 'Yann LeCun'",
                func=self._search_google_scholar
            ),
            Tool(
                name="paper_analyzer",
                description="Analyze and summarize a research paper from its URL. Input should be the paper URL.",
                func=self._analyze_paper
            )
        ]
    
    def _create_research_agent(self):
        """Create research-focused agent"""
        prompt_template = """
        You are an academic research assistant AI. Help users research papers and authors.

        Available tools:
        {tools}

        Tool names: {tool_names}

        Use this format:
        Question: the research question
        Thought: think about the best research approach
        Action: the action to take (use one of: {tool_names})
        Action Input: the input to the action
        Observation: the result of the action
        ... (repeat as needed)
        Thought: I have found the papers, now I should present them to the user
        Final Answer: List all papers found and ask user which one to analyze

        Question: {input}
        Thought: {agent_scratchpad}
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["input", "tools", "tool_names", "agent_scratchpad"]
        )
        
        return create_react_agent(self.llm, self.tools, prompt)
    
    def research_papers_interactive(self, author_name: str) -> Dict[str, Any]:
        """Interactive research method that shows papers first, then analyzes chosen one"""
        start_time = time.time()
        
        try:
            print(f"\n🎓 Academic Research Agent processing: {author_name}")
            
            # Step 1: Search for papers
            print(f"\n📚 **Step 1: Finding papers by {author_name}**")
            papers_result = self._search_google_scholar(author_name)
            
            # Parse papers and extract URLs
            paper_urls = []
            paper_titles = []
            
            if "🔗" in papers_result:
                lines = papers_result.split('\n')
                current_title = None
                
                for line in lines:
                    line = line.strip()
                    if line and line[0].isdigit() and '. ' in line:
                        # This is a title line
                        current_title = line.split('. ', 1)[1] if '. ' in line else line
                        paper_titles.append(current_title)
                    elif line.startswith('🔗 '):
                        # This is a URL line
                        url = line.replace('🔗 ', '').strip()
                        paper_urls.append(url)
            
            # Display papers
            print(papers_result)
            
            # If no papers found, return early
            if not paper_titles:
                return {
                    "findings": f"No papers found for {author_name}",
                    "research_time": time.time() - start_time,
                    "status": "no_papers_found"
                }
            
            # Step 2: Interactive paper selection
            print(f"\n📋 **Step 2: Choose a paper to analyze in detail**")
            print(f"Found {len(paper_titles)} paper(s). Which would you like me to analyze?")
            
            # Show numbered options
            for i, title in enumerate(paper_titles, 1):
                print(f"{i}. {title}")
            
            print(f"{len(paper_titles) + 1}. Skip detailed analysis")
            
            # Get user choice
            while True:
                try:
                    choice = input(f"\nEnter your choice (1-{len(paper_titles) + 1}): ").strip()
                    
                    if not choice:
                        continue
                        
                    choice_num = int(choice)
                    
                    if choice_num == len(paper_titles) + 1:
                        # Skip analysis
                        return {
                            "findings": f"Papers by {author_name}:\n\n{papers_result}\n\n📋 Analysis skipped by user choice.",
                            "research_time": time.time() - start_time,
                            "status": "analysis_skipped"
                        }
                    elif 1 <= choice_num <= len(paper_titles):
                        selected_title = paper_titles[choice_num - 1]
                        selected_url = paper_urls[choice_num - 1] if choice_num - 1 < len(paper_urls) else None
                        break
                    else:
                        print(f"❌ Please enter a number between 1 and {len(paper_titles) + 1}")
                        
                except ValueError:
                    print("❌ Please enter a valid number")
                except KeyboardInterrupt:
                    return {
                        "findings": f"Research interrupted by user",
                        "research_time": time.time() - start_time,
                        "status": "interrupted"
                    }
            
            # Step 3: Analyze selected paper
            print(f"\n📄 **Step 3: Analyzing selected paper**")
            print(f"🎯 **Selected:** {selected_title}")
            
            if selected_url:
                print(f"🔗 **URL:** {selected_url}")
                analysis_result = self._analyze_paper(selected_url)
            else:
                analysis_result = f"❌ No accessible URL found for this paper. Analysis not possible."
            
            # Step 4: Compile final results
            final_results = f"""📚 **Research Summary for {author_name}:**

{papers_result}

📄 **Detailed Analysis of Selected Paper:**
**Title:** {selected_title}

{analysis_result}"""
            
            elapsed = time.time() - start_time
            return {
                "findings": final_results,
                "research_time": elapsed,
                "status": "research_complete"
            }
            
        except Exception as e:
            return {
                "findings": f"Research error: {str(e)}",
                "research_time": time.time() - start_time,
                "status": "research_failed"
            }
    
    def research(self, query: str) -> Dict[str, Any]:
        """Main research method"""
        start_time = time.time()
        
        try:
            print(f"\n🎓 Academic Research Agent processing: {query}")
            result = self.agent_executor.invoke({"input": query})
            
            elapsed = time.time() - start_time
            return {
                "findings": result["output"],
                "research_time": elapsed,
                "status": "research_complete"
            }
            
        except Exception as e:
            return {
                "findings": f"Research error: {str(e)}",
                "research_time": time.time() - start_time,
                "status": "research_failed"
            }
    
    def _search_google_scholar(self, author_name: str) -> str:
        """Search Google Scholar for author's papers"""
        print(f"📚 Searching Google Scholar for: {author_name}")
        
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # More precise Google Scholar search with author quotes
                search_url = f'https://scholar.google.com/scholar?q=author:"{author_name.replace(" ", "+")}"&hl=en'
                print(f"🔍 Search URL: {search_url}")
                page.goto(search_url, wait_until="networkidle", timeout=15000)
                
                # Wait for results
                try:
                    page.wait_for_selector('.gs_rt', timeout=10000)
                except:
                    print("⚠️ No results found or page didn't load properly")
                    browser.close()
                    return f"No search results found for {author_name} on Google Scholar"
                
                # Extract paper information with better filtering
                results = page.query_selector_all('.gs_r')[:10]  # Get more results to filter
                print(f"🔍 Found {len(results)} raw results to process")
                
                if results:
                    author_results = f"📖 Papers by {author_name}:\n\n"
                    paper_links = []
                    valid_papers = 0
                    
                    for i, result in enumerate(results):
                        try:
                            # Get title and link from result
                            title_element = result.query_selector('.gs_rt a')
                            if not title_element:
                                print(f"⚠️ Result {i+1}: No title element found")
                                continue
                                
                            title = title_element.inner_text().strip()
                            url = title_element.get_attribute('href')
                            
                            print(f"📄 Result {i+1}: {title[:60]}...")
                            
                            # Get author information to verify relevance
                            author_element = result.query_selector('.gs_a')
                            author_text = author_element.inner_text() if author_element else ""
                            
                            print(f"👥 Authors found: {author_text[:100]}...")
                            
                            # More lenient filtering: check if any part of the searched name appears
                            author_name_parts = author_name.lower().split()
                            author_text_lower = author_text.lower()
                            
                            # Check different name combinations
                            name_variations = [
                                author_name.lower(),  # Full name
                                " ".join(author_name_parts[-2:]) if len(author_name_parts) >= 2 else author_name.lower(),  # Last two parts
                                author_name_parts[-1] if author_name_parts else "",  # Last name only
                            ]
                            
                            # Add initials + last name for academic papers (e.g., "T Goodluck Constance")
                            if len(author_name_parts) >= 2:
                                initials_last = f"{author_name_parts[0][0].lower()} {' '.join(author_name_parts[1:]).lower()}"
                                name_variations.append(initials_last)
                            
                            # Check if any variation matches
                            is_relevant = any(variation in author_text_lower for variation in name_variations if variation)
                            
                            print(f"🔍 Checking variations: {name_variations}")
                            print(f"✅ Relevant: {is_relevant}")
                            
                            # Additional check: avoid obviously unrelated papers
                            unrelated_keywords = ['user profiles', 'profiles for author', 'author:', 'citations?view_op']
                            is_unrelated = any(keyword in title.lower() for keyword in unrelated_keywords)
                            
                            if is_relevant and not is_unrelated and valid_papers < 8:  # Allow more papers
                                valid_papers += 1
                                author_results += f"{valid_papers}. {title}\n"
                                
                                # Show authors if available
                                if author_text:
                                    # Clean up author text (remove extra info)
                                    clean_authors = author_text.split('-')[0].split('…')[0].strip()
                                    author_results += f"   👥 Authors: {clean_authors}\n"
                                
                                if url and not url.startswith('https://scholar.google.com/citations'):
                                    author_results += f"   🔗 {url}\n"
                                    paper_links.append(url)
                                
                                author_results += "\n"
                            else:
                                print(f"❌ Filtered out: relevant={is_relevant}, unrelated={is_unrelated}")
                                
                        except Exception as e:
                            print(f"❌ Error processing result {i+1}: {e}")
                            continue
                    
                    if valid_papers > 0:
                        author_results += f"📋 Found {valid_papers} relevant papers"
                        if paper_links:
                            author_results += f" with {len(paper_links)} accessible for analysis."
                            # Store first paper link for potential analysis
                            self._latest_paper_url = paper_links[0]
                        else:
                            author_results += "."
                        
                        browser.close()
                        return author_results
                    else:
                        print("❌ No relevant papers found after filtering")
                        browser.close()
                        
                        # Fallback: try a broader search
                        print("🔄 Trying broader search...")
                        return self._search_google_scholar_broad(author_name)
                
                browser.close()
                return f"No search results found for {author_name} on Google Scholar"
                
        except ImportError:
            return "Playwright not installed. Please install: pip install playwright && playwright install chromium"
        except Exception as e:
            print(f"❌ Scholar search error: {e}")
            return f"Scholar search failed: {str(e)}. This might be due to Google Scholar rate limiting or network issues."
    
    def _search_google_scholar_broad(self, author_name: str) -> str:
        """Fallback broader search for author's papers"""
        print(f"📚 Trying broader search for: {author_name}")
        
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Broader search without strict author quotes
                search_url = f'https://scholar.google.com/scholar?q={author_name.replace(" ", "+")}&hl=en'
                print(f"🔍 Broad search URL: {search_url}")
                page.goto(search_url, wait_until="networkidle", timeout=15000)
                
                # Wait for results
                page.wait_for_selector('.gs_rt', timeout=10000)
                
                # Extract first few results with minimal filtering
                results = page.query_selector_all('.gs_r')[:5]
                
                if results:
                    author_results = f"📖 Papers related to {author_name}:\n\n"
                    paper_links = []
                    
                    for i, result in enumerate(results, 1):
                        try:
                            title_element = result.query_selector('.gs_rt a')
                            if title_element:
                                title = title_element.inner_text().strip()
                                url = title_element.get_attribute('href')
                                
                                # Get author info
                                author_element = result.query_selector('.gs_a')
                                author_text = author_element.inner_text() if author_element else ""
                                
                                # Basic filtering - just remove obvious non-papers
                                unrelated_keywords = ['user profiles', 'profiles for author']
                                is_unrelated = any(keyword in title.lower() for keyword in unrelated_keywords)
                                
                                if not is_unrelated:
                                    author_results += f"{i}. {title}\n"
                                    
                                    if author_text:
                                        clean_authors = author_text.split('-')[0].split('…')[0].strip()
                                        author_results += f"   👥 Authors: {clean_authors}\n"
                                    
                                    if url and not url.startswith('https://scholar.google.com/citations'):
                                        author_results += f"   🔗 {url}\n"
                                        paper_links.append(url)
                                    
                                    author_results += "\n"
                        except:
                            continue
                    
                    author_results += f"📋 Found {len(paper_links)} papers (broader search)"
                    if paper_links:
                        self._latest_paper_url = paper_links[0]
                    
                    browser.close()
                    return author_results
                
                browser.close()
                return f"No papers found for {author_name} even with broader search"
                
        except Exception as e:
            print(f"❌ Broad search failed: {e}")
            return f"Both precise and broad searches failed for {author_name}"
    
    def _analyze_paper(self, paper_url: str) -> str:
        """Analyze and summarize a research paper"""
        print(f"📄 Analyzing paper: {paper_url[:50]}...")
        
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Navigate to paper
                page.goto(paper_url, wait_until="networkidle", timeout=15000)
                time.sleep(3)  # Let page fully load
                
                # Try to extract paper content
                content = self._extract_paper_content(page)
                
                browser.close()
                
                if content:
                    # Use Ollama to summarize
                    summary_prompt = f"""
                    Analyze this research paper content and provide a structured summary:
                    
                    {content}
                    
                    Please provide:
                    1. Main research question/problem
                    2. Key methodology or approach
                    3. Major findings/contributions
                    4. Significance to the field
                    
                    Keep the summary concise but informative.
                    """
                    
                    summary = self.llm.invoke(summary_prompt)
                    
                    return f"""📋 **Paper Analysis:**

{summary}

🔗 **Source:** {paper_url}
⏰ **Analyzed:** {datetime.datetime.now().strftime('%H:%M:%S')}"""
                
                return f"Could not extract content from: {paper_url}"
                
        except Exception as e:
            return f"Paper analysis failed: {str(e)}"
    
    def _extract_paper_content(self, page) -> str:
        """Extract text content from paper page"""
        try:
            # Try different selectors for paper content
            content_selectors = [
                '.ltx_abstract',  # arXiv abstract
                '#abstract',      # Many journal abstracts
                '.abstract',      # Generic abstract
                'article p',      # Article paragraphs
                '.content p',     # Content paragraphs
                'p'               # Any paragraphs
            ]
            
            extracted_content = ""
            
            for selector in content_selectors:
                try:
                    elements = page.query_selector_all(selector)
                    if elements and len(elements) > 0:
                        for element in elements[:5]:  # First 5 relevant elements
                            text = element.inner_text().strip()
                            if len(text) > 50:  # Only substantial text
                                extracted_content += f"{text}\n\n"
                        
                        if len(extracted_content) > 200:  # Enough content found
                            break
                except:
                    continue
            
            return extracted_content[:1500] if extracted_content else ""  # Limit length
            
        except Exception as e:
            print(f"Content extraction error: {e}")
            return ""

def demo_research_agent():
    """Demonstrate the academic research agent with provider selection"""
    
    print("🎓 ACADEMIC RESEARCH AGENT DEMO")
    print("=" * 60)
    print("🤖 Multi-Provider AI Research Assistant")
    print("=" * 60)
    
    # Provider selection
    print("\n🔧 **Choose your AI provider:**")
    print("1. 🦙 Ollama (Local, Free)")
    print("2. 🤖 OpenAI (Cloud, Paid)")
    print("3. 🧠 Anthropic (Cloud, Paid)")
    print("4. ⚙️  Custom Configuration")
    
    while True:
        provider_choice = input("\nSelect provider (1-4): ").strip()
        
        try:
            if provider_choice == "1":
                # Ollama setup
                model = input("Enter Ollama model (default: llama3.2): ").strip() or "llama3.2"
                agent = AcademicResearchAgent.create_ollama_agent(model=model)
                break
                
            elif provider_choice == "2":
                # OpenAI setup
                model = input("Enter OpenAI model (default: gpt-4): ").strip() or "gpt-4"
                api_key = input("Enter OpenAI API key (or press Enter to use env var): ").strip() or None
                agent = AcademicResearchAgent.create_openai_agent(model=model, api_key=api_key)
                break
                
            elif provider_choice == "3":
                # Anthropic setup
                model = input("Enter Anthropic model (default: claude-3-sonnet-20240229): ").strip() or "claude-3-sonnet-20240229"
                api_key = input("Enter Anthropic API key (or press Enter to use env var): ").strip() or None
                agent = AcademicResearchAgent.create_anthropic_agent(model=model, api_key=api_key)
                break
                
            elif provider_choice == "4":
                # Custom configuration
                provider = input("Enter provider (ollama/openai/anthropic): ").strip()
                model = input("Enter model name: ").strip()
                api_key = input("Enter API key (if needed): ").strip() or None
                agent = AcademicResearchAgent(provider=provider, model=model, api_key=api_key)
                break
                
            else:
                print("❌ Please enter 1, 2, 3, or 4")
                continue
                
        except Exception as e:
            print(f"❌ Setup error: {e}")
            print("Please try again or choose a different provider.")
            continue
    
    # Interactive researcher selection
    print("\n🔬 **Interactive Academic Research Demo**")
    print("💡 **Popular AI Researchers you could try:**")
    print("   • Geoffrey Hinton (Deep Learning pioneer)")
    print("   • Yann LeCun (CNN inventor, Meta AI)")
    print("   • Fei-Fei Li (Computer Vision expert)")
    print("   • Andrew Ng (Online education, former Stanford)")
    print("   • Yoshua Bengio (Neural Networks, Turing Award)")
    print("   • Demis Hassabis (DeepMind founder)")
    print("   • Or any researcher you're curious about!")
    
    # Get researcher name from user
    while True:
        researcher_name = input(f"\n👨‍🔬 Enter researcher name to search: ").strip()
        
        if not researcher_name:
            print("❌ Please enter a researcher name!")
            continue
        
        if researcher_name.lower() in ['quit', 'exit', 'q']:
            print("👋 Exiting demo. Goodbye!")
            return
        
        # Confirm the search
        confirm = input(f"🔍 Search for papers by '{researcher_name}'? (y/n): ").lower()
        if confirm in ['y', 'yes', '']:
            break
        elif confirm in ['n', 'no']:
            print("Let's try a different researcher...")
            continue
    
    print(f"\n{'='*60}")
    print(f"🔍 **Researching:** {researcher_name}")
    print(f"{'='*60}")
    
    # Perform interactive research
    print(f"🤖 Starting interactive research process...")
    results = agent.research_papers_interactive(researcher_name)
    
    print(f"\n{'='*60}")
    print(f"📋 **Final Research Summary:**")
    print(f"{'='*60}")
    print(results["findings"])
    print(f"\n⏱️ **Total research time:** {results['research_time']:.2f} seconds")
    print(f"📊 **Status:** {results['status']}")
    
    # Ask if they want to try another researcher
    print(f"\n🎯 **Want to research another academic?**")
    while True:
        another = input("Try another researcher? (y/n): ").lower()
        if another in ['y', 'yes']:
            print(f"\n{'-'*40}")
            demo_research_agent()  # Recursive call for another search
            break
        elif another in ['n', 'no']:
            print("👋 Thank you for using the Academic Research Agent!")
            break
        else:
            print("Please enter 'y' for yes or 'n' for no")

def interactive_research_mode():
    """Continuous interactive research mode with provider selection"""
    print("🔄 INTERACTIVE RESEARCH MODE")
    print("=" * 50)
    print("💡 Research multiple academics in one session!")
    print("=" * 50)
    
    # Provider selection (same as demo mode)
    print("\n🔧 **Choose your AI provider:**")
    print("1. 🦙 Ollama (Local, Free)")
    print("2. 🤖 OpenAI (Cloud, Paid)")
    print("3. 🧠 Anthropic (Cloud, Paid)")
    
    while True:
        provider_choice = input("\nSelect provider (1-3): ").strip()
        
        try:
            if provider_choice == "1":
                agent = AcademicResearchAgent.create_ollama_agent()
                break
            elif provider_choice == "2":
                agent = AcademicResearchAgent.create_openai_agent()
                break
            elif provider_choice == "3":
                agent = AcademicResearchAgent.create_anthropic_agent()
                break
            else:
                print("❌ Please enter 1, 2, or 3")
                continue
        except Exception as e:
            print(f"❌ Setup error: {e}")
            return
    
    while True:
        print(f"\n🔬 **Who would you like to research?**")
        researcher_name = input(f"👨‍🔬 Enter researcher name (or 'quit' to exit): ").strip()
        
        if not researcher_name:
            print("❌ Please enter a researcher name!")
            continue
        
        if researcher_name.lower() in ['quit', 'exit', 'q', 'done']:
            print("👋 Exiting interactive mode. Goodbye!")
            break
        
        print(f"\n🔍 **Researching:** {researcher_name}")
        print(f"{'='*50}")
        
        # Perform research
        results = agent.research_papers_interactive(researcher_name)
        
        print(f"\n📋 **Research Complete:**")
        print(results["findings"])
        print(f"\n⏱️ **Research time:** {results['research_time']:.2f} seconds")
        
        print(f"\n{'-'*50}")

def lecture_demo_mode():
    """Optimized mode for live lecture demonstrations with provider selection"""
    
    print("🎓 LECTURE DEMO MODE")
    print("=" * 50)
    print("🎯 **Perfect for Live Demonstrations**")
    print("💫 **Interactive Demo Flow:**")
    print("   1. Choose AI provider for demo")
    print("   2. Ask audience for researcher suggestions")
    print("   3. Show all papers by that researcher")
    print("   4. Let audience vote on which paper to analyze")
    print("   5. AI analyzes and presents findings")
    print("   6. Discuss results with audience")
    print("=" * 50)
    
    # Quick provider selection for lecture
    print(f"\n🎤 **Select AI Provider for Live Demo:**")
    print("1. 🦙 Ollama (Local, No Internet Required)")
    print("2. 🤖 OpenAI (Cloud, High Performance)")
    print("3. 🧠 Anthropic (Cloud, High Quality)")
    
    while True:
        provider_choice = input("\nQuick select (1-3): ").strip()
        
        try:
            if provider_choice == "1":
                agent = AcademicResearchAgent.create_ollama_agent()
                break
            elif provider_choice == "2":
                agent = AcademicResearchAgent.create_openai_agent()
                break
            elif provider_choice == "3":
                agent = AcademicResearchAgent.create_anthropic_agent()
                break
            else:
                print("❌ Please enter 1, 2, or 3")
                continue
        except Exception as e:
            print(f"❌ Setup error: {e}")
            return
    
    # Suggested researchers for quick demo
    print(f"\n💡 **Quick Demo Suggestions:**")
    suggestions = [
        "Geoffrey Hinton", "Yann LeCun", "Fei-Fei Li", 
        "Andrew Ng", "Yoshua Bengio", "Demis Hassabis"
    ]
    
    for i, name in enumerate(suggestions, 1):
        print(f"   {i}. {name}")
    
    print(f"\n🎤 **For Live Demo:**")
    
    while True:
        print(f"\n👥 Ask your audience: 'Which AI researcher should we investigate?'")
        researcher_name = input(f"🎯 Enter researcher name from audience suggestion: ").strip()
        
        if not researcher_name:
            print("⏸️  Waiting for audience suggestion...")
            continue
        
        if researcher_name.lower() in ['quit', 'exit', 'done']:
            print("🎉 Lecture demo complete!")
            break
        
        # Quick confirmation for lecture pace
        print(f"\n📢 **Announcing to audience:** 'Let's research {researcher_name}!'")
        input("Press Enter when ready to start demo... ")
        
        print(f"\n🔴 **LIVE DEMO IN PROGRESS**")
        print(f"🔍 Researching: {researcher_name}")
        print(f"{'='*50}")
        
        # Execute interactive research for live audience
        print(f"🎤 **[Tell audience: 'Watch the AI find and analyze real research papers!']**")
        results = agent.research_papers_interactive(researcher_name)
        
        # Present results to audience
        print(f"\n📋 **LIVE RESULTS FOR AUDIENCE:**")
        print("🎤 **[Present these findings to your audience]**")
        print("=" * 50)
        print(results["findings"])
        print("=" * 50)
        print(f"⏱️ **Demo completed in:** {results['research_time']:.2f} seconds")
        
        # Audience interaction prompt
        print(f"\n🎤 **Audience Discussion Points:**")
        print(f"   • 'What do you think about these research findings?'")
        print(f"   • 'How could AI help researchers like this?'")
        print(f"   • 'Did the AI correctly identify relevant papers?'")
        print(f"   • 'Should we investigate another researcher?'")
        
        # Continue or finish
        continue_demo = input(f"\n🔄 Continue with another researcher? (y/n): ").lower()
        if continue_demo not in ['y', 'yes']:
            print("🎉 Lecture demo session complete!")
            break

if __name__ == "__main__":
    print("🎓 **ACADEMIC RESEARCH AGENT - MULTI-PROVIDER VERSION**")
    print("🤖 Supports: Ollama (Local) | OpenAI (Cloud) | Anthropic (Cloud)")
    print("=" * 70)
    print("Choose your mode:")
    print("1. 🎯 Single Research Demo")
    print("2. 🔄 Interactive Research Mode") 
    print("3. 🎤 Lecture Demo Mode")
    print("4. 🧪 Quick Test (Ollama)")
    
    while True:
        choice = input("\nSelect mode (1-4): ").strip()
        
        if choice == "1":
            demo_research_agent()
            break
        elif choice == "2":
            interactive_research_mode()
            break
        elif choice == "3":
            lecture_demo_mode()
            break
        elif choice == "4":
            # Quick test with Ollama
            try:
                print("\n🧪 Quick test with Ollama...")
                agent = AcademicResearchAgent.create_ollama_agent()
                researcher_name = input("Enter researcher name for quick test: ").strip()
                if researcher_name:
                    results = agent.research_papers_interactive(researcher_name)
                    print(f"\n✅ Test complete! Status: {results['status']}")
            except Exception as e:
                print(f"❌ Test failed: {e}")
            break
        else:
            print("❌ Please enter 1, 2, 3, or 4")