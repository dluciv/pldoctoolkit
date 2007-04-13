package org.spbu.pldoctoolkit.editors;

import org.eclipse.jface.text.rules.*;

public class XMLPartitionScanner extends RuleBasedPartitionScanner {
	public final static String XML_COMMENT = "__xml_comment";
	public final static String XML_TAG = "__xml_tag";

	public XMLPartitionScanner() {
		IPredicateRule[] rules = new IPredicateRule[2];
		
		rules[0] = new MultiLineRule("<!--", "-->", new Token(XML_COMMENT));
		rules[1] = new TagRule(new Token(XML_TAG));

		setPredicateRules(rules);
	}
}
