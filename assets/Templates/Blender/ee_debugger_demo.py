from web_enhanced_debugger import WebEnhancedDebuggerAgent

# Initialize the debugger with CodeLlama model
debugger = WebEnhancedDebuggerAgent(model="codellama:latest")

# Example error captured from Trae.ai logs
error_msg = "sqlite3.OperationalError: no such column: search_keywords"

print("=== Web - Enhanced Debugger Demo ===")
print(f"\n🐞 Processing Error: {error_msg}")

# Use the enhanced debugging method for better analysis
fix_suggestion = debugger.enhanced_debug_and_fix(error_msg)
print(fix_suggestion)

print("\\n" + "=" * 50)
print("✅ Debugging completed!")
print("The debugger provided=")
print("   • Error categorization")
print("   • Web search results")
print("   • AI - powered fix suggestion")
print("   • Prevention recommendations")
