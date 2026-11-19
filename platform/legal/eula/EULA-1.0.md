# Blindsight Endpoint Licence Agreement

Version 1.0, effective 18 November 2026

**1. Parties, scope and acceptance**

1.1 This Licence Agreement (the "Agreement") is made between Blindsight Technologies AG, Rennweg 57, 8001 Zurich, Switzerland, UID CHE-484.046.837 ("Blindsight"), and the organisation that subscribes to the Service and accepts this Agreement (the "Customer").

1.2 The Customer accepts this Agreement when (a) a person authorised by the Customer accepts it in the Blindsight console, (b) the Customer signs an order form or other agreement that refers to it, or (c) the Customer, through a person authorised by it, installs the Software after this Agreement was made available to it, whichever occurs first. The person who accepts confirms that they are authorised to bind the Customer.

1.3 Acceptance covers every installation of the Software on devices of the Customer, including installations made silently, through device management tools or by automatic update, which do not display this Agreement.

1.4 Persons who use a device on which the Customer has installed the Software ("Authorised Users") use the Software on the Customer's behalf. They are not parties to this Agreement and acquire no licence of their own. The Customer is responsible for their use of the Software. A confirmation shown to a person on a device is a notice only and does not make that person a party to this Agreement.

1.5 The Software and the Service are provided for business purposes only and are not offered to consumers.

1.6 Where a managed service provider, reseller or other partner of Blindsight (a "Partner") accepts this Agreement or manages the Service for the Customer, the Partner confirms that it is authorised by the Customer to do so. The Customer is bound by that acceptance, and the Partner is responsible to Blindsight for its own acts and omissions.

**2. Definitions**

In this Agreement:
(a) "Software" means the Blindsight desktop software for Windows ("Blindsight Endpoint") and for macOS ("Blindsight Mac") in object code form, including updates and the Documentation, but not the Third-Party Components;
(b) "Service" means Blindsight's hosted platform and console, provided under the Service Terms;
(c) "Service Terms" means the master agreement, order form or online subscription terms under which the Customer subscribes to the Service;
(d) "DPA" means the data processing agreement between Blindsight and the Customer published at https://blindsight.io/platform/legal/dpa or signed by the parties;
(e) "Documentation" means the user and administrator documentation for the Software and the Service published by Blindsight;
(f) "Customer Data" means data that the Software or the Service processes on the Customer's behalf, including personal data of Authorised Users;
(g) "Third-Party Components" means the components listed in the file THIRD_PARTY_NOTICES.md supplied with the Software, and the Model Files;
(h) "Model Files" means the files of the on-device name detection model that the Software downloads when the Customer enables that function, as described in clause 6.8;
(i) "Subscription Term" means the period for which the Customer has subscribed to the Service, including any period of evaluation or trial.

**3. Licence**

3.1 Subject to this Agreement, Blindsight grants the Customer a non-exclusive, non-transferable and non-sublicensable licence, for the Subscription Term, to install and use the Software on devices that the Customer owns or controls, up to the number of devices or users stated in the Customer's order, solely for the Customer's internal business purposes and in accordance with the Documentation. The Customer may allow its affiliates to use the Software under this Agreement and remains responsible for them.

3.2 The Software is licensed, not sold. Blindsight and its licensors retain all rights not expressly granted. The licence may be terminated only as clause 15 provides.

3.3 Third-Party Components are licensed to the Customer under their own licences as set out in clause 6.

**4. Licence limits and end of the licence**

4.1 Use of the Software is limited to the devices, users and functions in the Customer's order. If the Customer's use exceeds its order, the parties will settle the difference under the Service Terms.

4.2 When the Customer's subscription ends, the Service may apply notice and read-only periods as set out in the Service Terms or the Documentation. When the Service has recorded that the Customer's licence has ended, the Software removes itself from the traffic path of each device: it stops inspecting traffic, removes its proxy and routing settings and its root certificate from the device's trust stores, and stops sending records of its findings to the Service. It continues to check periodically whether the licence has been restored and, if so, resumes operation. It does not block the device's traffic. The Customer shall uninstall the Software if the licence is not restored.

**5. Restrictions and statutory rights**

5.1 Except as this Agreement (in particular clause 6) or mandatory law permits, the Customer shall not:
(a) copy the Software, except for installation, use in accordance with clause 3, and backup and archival copies;
(b) modify, adapt, translate or create derivative works of the Software;
(c) decompile, disassemble or otherwise reverse engineer the Software;
(d) sell, rent, lease, lend, sublicense, distribute or otherwise make the Software available to anyone other than its Authorised Users and Partners, or use it to provide services to third parties other than its affiliates;
(e) remove or alter any copyright, licence or other notice in the Software;
(f) use the Software to develop a competing product;
(g) publish the results of benchmark or security tests of the Software without Blindsight's prior written consent, which Blindsight will not withhold unreasonably. This does not restrict testing for the Customer's own purposes, or disclosure of results to the Customer's auditors, supervisory authorities or advisers; or
(h) use the Software in breach of clause 8 or of applicable law.

5.2 Nothing in this Agreement restricts rights that cannot be excluded by contract under applicable copyright law, including the Swiss Federal Act on Copyright and Related Rights and laws implementing Directive 2009/24/EC, in particular the right (a) to make a backup copy of the Software, (b) to observe, study or test the functioning of the Software while performing acts that the Customer is entitled to perform, and (c) to decompile the Software to the extent indispensable to obtain the information necessary for the interoperability of an independently created program, under the conditions set out in that law. Where the information necessary for interoperability is not readily available in the Documentation, the Customer may ask Blindsight for it, and Blindsight will provide it within 30 days, on reasonable terms and subject to clause 11, if it is available to Blindsight.

**6. Third-party components**

6.1 Open source components. The Software includes components licensed by their authors under open source licences. They are listed in the file THIRD_PARTY_NOTICES.md supplied with the Software and opened by "Legal notices" in the application, and the licence texts are in the "licenses" folder installed with the Software. Each such component is licensed under its own licence and not under this Agreement. Nothing in this Agreement restricts the rights that those licences grant. If this Agreement conflicts with such a licence for such a component, that licence prevails for that component.

6.2 LGPL components. Some components are licensed under the GNU Lesser General Public License version 2.1 or version 3 (the "LGPL Components"). Despite any other provision of this Agreement, including clauses 5 and 7, the Customer may (a) modify the LGPL Components, and modify or replace the files of the Software that contain them, for the Customer's own use, including to relink the Software with a modified version of an LGPL Component, and, to the extent section 6 of the LGPL version 2.1 requires it, modify the Software for the Customer's own use; and (b) reverse engineer the Software to the extent necessary to debug such modifications.

6.3 Source code. The complete corresponding source code of the LGPL Components, at the version supplied to the Customer, and the materials needed to relink those that are statically linked, are available at https://downloads.blindsight.io/oss/ followed by the version number of the Software (for example https://downloads.blindsight.io/oss/2.1.10/), the same place from which the installers are downloaded. Some of them are also included in the "licenses/source" folder installed with the Software. For at least three years from the date the Customer received a version of the Software, and for as long as Blindsight distributes that version, Blindsight will also supply that source code on a physical medium or by download, for no more than the cost of performing this distribution, on written request to legal@blindsight.io or to Blindsight Technologies AG, Legal, Rennweg 57, 8001 Zurich, Switzerland. This offer is open to anyone who received the Software.

6.4 Modified components. Software in which the Customer has modified or replaced a component is outside Blindsight's support and warranty to the extent the modification causes a fault. This does not terminate the licence and does not restrict modification under clause 6.2.

6.5 Microsoft runtime files. The Windows version of the Software includes runtime files from Microsoft Corporation (the "Microsoft Files"). They are licensed, not sold. The Customer may use the Microsoft Files only as part of the Software, and may not distribute them separately or use them with other software. The Customer may not reverse engineer, decompile or disassemble the Microsoft Files, except to the extent that applicable law permits despite this limitation. The Microsoft Files are provided "as is"; Microsoft and its suppliers give no warranty for them and are not liable for any damage arising from them, to the extent the law permits. These terms protect the Microsoft Files at least as much as the Microsoft licence terms under which Blindsight distributes them. No right is given to use Microsoft's name or trademarks, and nothing in the Software states or implies that Microsoft endorses it. The Microsoft Files are not licensed under any open source licence, and clauses 6.1 to 6.4 do not apply to them.

6.6 Wintun. The Windows version of the Software includes the file wintun.dll from WireGuard LLC, which is licensed under the WireGuard LLC Prebuilt Binaries License reproduced in the "licenses" folder. The Customer may use it only as part of the Software. The Customer may not reverse engineer, decompile, disassemble, modify or separately distribute it, except to the extent that applicable law permits despite this limitation. It is provided "as is", and WireGuard LLC gives no warranty for it and is not liable for any damage arising from it, to the extent the law permits.

6.7 WebView2 SDK. The Windows version of the Software includes the Microsoft WebView2 SDK files (WebView2Loader.dll and the Microsoft.Web.WebView2 assemblies), which are licensed under Microsoft's BSD-style licence. Its copyright notice, conditions and disclaimer are reproduced in the "licenses" folder. The Microsoft and WebView2 names are not used to endorse the Software. The WebView2 Runtime is not part of the Software; it is a Microsoft component already present on the device or installed from Microsoft.

6.8 Model Files. If the Customer enables on-device name detection, the Software downloads the Model Files (model.onnx and tokenizer.json, with a NOTICE.txt file naming their sources). The files model.onnx and tokenizer.json are licensed under the Creative Commons Attribution-ShareAlike 4.0 International licence (CC BY-SA 4.0), whose text is in the "licenses" folder, and not under this Agreement. Clauses 5 and 7 do not apply to them, and nothing in this Agreement restricts the rights that CC BY-SA 4.0 grants for them. That licence covers the Model Files only and does not extend to the Software. The attribution for the Model Files is in NOTICE.txt and in THIRD_PARTY_NOTICES.md.

**7. Integrity of the Software**

The Customer shall not disable, bypass or tamper with the Software's licence checks, update verification, uninstall protection or integrity monitoring, except (a) as clause 6 permits, (b) through the settings provided in the Service or described in the Documentation, or (c) as mandatory law permits. Installing, updating, configuring and removing the Software through the Customer's usual device management tools is permitted. If the Customer replaces an LGPL Component under clause 6.2, the Software's integrity monitoring may report the change to the Customer's administrators; Blindsight will not treat that change as a breach of this Agreement.

**8. Operation of the Software and the Customer's responsibilities**

8.1 What the Software does. To protect data sent to AI services, the Software, once installed and enrolled in the Service:
(a) creates a root certificate on each device, adds it to the device's certificate trust stores, and uses it to decrypt and inspect encrypted traffic to the AI services selected by the Customer's policy in the Service; it does not inspect the content of sign-in and identity pages;
(b) depending on the operating system and the Customer's settings, directs that traffic through a local proxy, a virtual network adapter or a packet filter driver installed on the device;
(c) detects personal data and other sensitive information in that traffic on the device and, according to the Customer's policy, allows, flags, redacts, pseudonymises or blocks it;
(d) sends to the Service identifiers of the device and of its user, status information and records of its findings, including the names of files submitted to AI services, and, where the Customer's policy allows text to leave the device (which is the default setting), the text of prompts, replies, system instructions, tool results and files submitted to AI services, after redaction on the device; the Service analyses that text for security threats, sensitive information and the Customer's rules, as described in the DPA; and
(e) checks for and installs updates under clause 9.
The Documentation describes these functions and the settings that control them.

8.2 The Customer's responsibilities. The Customer decides whether, where and how to deploy the Software and how to configure the Service, and is responsible for:
(a) having a lawful basis under applicable data protection law for the processing of personal data by means of the Software and the Service;
(b) informing Authorised Users and other persons concerned, before the Software is used on their devices, in a clear and accessible way, of what the Software inspects, what is recorded and who can see it;
(c) informing and consulting, or obtaining the agreement of, works councils, staff representatives, trade unions or authorities where applicable law or collective agreements require it;
(d) carrying out any data protection impact assessment that applicable law requires;
(e) its policy settings in the Service, including which services are inspected, how identities are displayed, how long data is kept and whether text may leave devices; and
(f) its rules on the private use of devices and AI services.
Blindsight provides the Documentation and reasonable assistance as set out in the DPA.

8.3 Intended purpose. The Software and the Service are intended to protect personal data, confidential information and the security of the Customer's systems when AI services are used. They are not designed or intended to evaluate the performance, productivity or behaviour of individuals, to infer emotions, or to take or support decisions on recruitment, promotion, termination, task allocation or other terms of work. The Customer shall not use them for those purposes. Detection uses rules and statistical models; it will not detect every item of sensitive information and may flag information that is not sensitive.

8.4 Acceptable use. The Customer shall not use the Software (a) on devices that it does not own or control, or to inspect the traffic of persons who are not Authorised Users, (b) to intercept communications or monitor individuals in breach of applicable law, or (c) to use the device root certificate or its private key for any purpose other than the operation of the Software.

**9. Updates and support**

9.1 Automatic updates are enabled by default. The Customer can control automatic installation for managed devices in the Service, and the update channel and installation through its device management tools. Updates are signed by Blindsight and verified by the Software before they are installed.

9.2 Blindsight provides security updates for the Software for a support period of at least five years from the date it first made the Software available, and in any case during the Subscription Term. Security updates are delivered in new versions of the Software, and Blindsight supports each version until twelve months after a newer version is released. The Customer should install updates promptly. Blindsight is not responsible for a defect that an update made available to the Customer would have corrected, if the Customer did not install that update within a reasonable time.

9.3 Security vulnerabilities in the Software can be reported to security@blindsight.io.

**10. Data protection**

10.1 For personal data that the Software and the Service process on the Customer's behalf, the Customer is the controller (or a processor acting for its own controller) and Blindsight is the processor (or sub-processor). Blindsight processes that data only in accordance with the DPA, which forms part of this Agreement. The DPA describes the processing, the sub-processors (listed at https://blindsight.io/platform/legal/subprocessors), the locations of processing, the security measures and the transfer safeguards, and prevails over this Agreement for the processing of personal data.

10.2 Blindsight processes the contact, account, sign-in, licensing and billing data of the Customer's administrators, other users of the Blindsight console and contacts as a controller, as described in its privacy notice at https://blindsight.io/platform/legal/privacy.

10.3 Blindsight may use (a) technical data on the operation of the Software, such as versions, errors and performance, and (b) aggregated information that does not identify the Customer, any Authorised User or any other person, such as the names of AI services observed across several customers, to operate, secure and improve the Software and the Service. Blindsight does not use the text of prompts, replies or files processed for the Customer to train models or for any other purpose of its own.

**11. Confidentiality**

11.1 Each party shall keep confidential the non-public information that the other party discloses to it in connection with this Agreement and that is marked as confidential or should reasonably be understood to be confidential, use it only to perform this Agreement, and disclose it only to its employees, affiliates, advisers, auditors and subcontractors who need to know it and are bound by equivalent obligations.

11.2 This clause does not apply to information that is or becomes public without breach of this Agreement, that the receiving party already lawfully had or independently developed, or that it lawfully receives from a third party without a duty of confidentiality. A party may disclose confidential information where law, a court or a supervisory authority requires it, and shall, where lawful, tell the other party beforehand.

11.3 These obligations continue for five years after this Agreement ends, and for trade secrets for as long as they remain trade secrets. Personal data is governed by the DPA.

**12. Warranty**

12.1 Blindsight warrants to the Customer that during the paid Subscription Term the Software will perform materially as described in the Documentation. If it does not, and the Customer notifies Blindsight, Blindsight will correct the Software or provide a workaround within a reasonable time. If Blindsight cannot do so, either party may terminate the affected subscription, and Blindsight will refund the fees prepaid for the remainder of the Subscription Term.

12.2 Except as stated in clause 12.1, and to the extent the law permits, the Software is provided "as is" and "as available". Blindsight does not warrant that the Software will operate without interruption or error, or that it will detect every threat or every item of sensitive information. Warranties implied by law are excluded to the extent the law permits. During any free evaluation or trial, the Software is provided only on the terms of this clause 12.2.

12.3 Nothing in this Agreement excludes or limits liability for defects that Blindsight has fraudulently concealed, or any other warranty right that cannot be excluded by law.

**13. Liability**

13.1 Nothing in this Agreement limits or excludes liability for unlawful intent or gross negligence, for death or personal injury, under mandatory product liability law, or any other liability that cannot be limited or excluded by law.

13.2 Subject to clause 13.1, neither party is liable for indirect or consequential loss, loss of profit, revenue or business, or business interruption. Liability for loss of data that the Customer keeps is limited to the reasonable cost of restoring it from the Customer's most recent backup. This limitation does not apply to Customer Data held in the Service, for which clause 13.3 applies.

13.3 Subject to clause 13.1, each party's total liability under or in connection with this Agreement, the Service Terms and the DPA together is limited to the greater of (a) the fees paid and payable by the Customer for the Software and the Service in the twelve months before the event giving rise to the liability and (b) CHF 100,000. This limit does not apply to the Customer's obligation to pay fees, or to its liability for breach of clauses 5, 7 or 14. The limit applies equally to claims for breach of data protection law, of the DPA or of clause 11.

13.4 Subject to clause 13.1, during any free evaluation or trial Blindsight's total liability is limited to CHF 10,000.

**14. Export control and sanctions**

14.1 The Software contains encryption technology and may be subject to export control and sanctions laws, including those of Switzerland and the European Union. The Customer shall comply with those laws and, where they apply to it, the export laws of the United States.

14.2 The Customer shall not export, re-export, transfer or make the Software available (a) to any country or territory, or to any person, subject to comprehensive sanctions or on a sanctions or restricted party list under those laws, or (b) for any end use prohibited by those laws, without the authorisation those laws require. The Customer is responsible for any import, use or re-export authorisation required in its own jurisdiction.

14.3 Blindsight may suspend the delivery of the Software or the Service to the extent necessary to comply with those laws and is not liable for that suspension.

**15. Term and termination**

15.1 This Agreement starts on acceptance under clause 1.2 and continues until the Subscription Term ends.

15.2 Either party may terminate this Agreement by written notice if the other party materially breaches it and does not cure the breach within 30 days of receiving notice. Termination rights in the Service Terms, and termination rights that law or a supervisory authority requires for the Customer, are unaffected.

15.3 When this Agreement ends: (a) the licence in clause 3 ends and the Software behaves as clause 4.2 describes; (b) the Customer shall uninstall the Software within 30 days; and (c) the Customer may export its Customer Data, and Blindsight will return and delete Customer Data, as the Service Terms and the DPA provide, with an export period of at least 30 days after the end.

15.4 Clauses 1.4, 5, 6, 7 (until the Software is uninstalled), 8.2 and 8.4 (for processing before the end), 10 (until Customer Data has been deleted), 11, 12.2, 12.3, 13, 14, 15.3, 15.4, 16, 19 and 20 survive. Ending this Agreement does not end any right that an open source licence or CC BY-SA 4.0 gives the Customer for a Third-Party Component.

**16. Verification of use**

The Customer agrees that Blindsight may rely on the device and user counts recorded by the Service. On Blindsight's reasonable request, not more than once in any twelve months, the Customer will confirm in writing that its use of the Software complies with its order.

**17. Regulated customers**

If the Customer is subject to Regulation (EU) 2022/2554 (DORA), to FINMA rules on outsourcing or operational resilience, or to similar rules for financial institutions, the parties will agree the additional terms that those rules require, including rights of access, information and audit for the Customer and its supervisory authorities, subcontracting conditions, locations of data processing, assistance with incidents, exit arrangements and termination rights, in the Service Terms or an addendum. Those terms prevail over this Agreement.

**18. Changes to this Agreement**

Blindsight may publish new versions of this Agreement. A new version applies to the Customer when a person authorised by the Customer accepts it in the Blindsight console or the parties sign it. Until then the version last accepted continues to apply, but Blindsight may require acceptance of the new version before further installer downloads, deployments or enrolments are made. Continued use of the Software is not acceptance of a new version.

**19. Governing law and courts**

19.1 This Agreement is governed by Swiss substantive law, excluding its conflict-of-laws rules and the United Nations Convention on Contracts for the International Sale of Goods.

19.2 The courts of Zurich, Switzerland, have exclusive jurisdiction, unless mandatory law provides otherwise.

19.3 If the Customer is domiciled neither in Switzerland nor in a state bound by the Lugano Convention, any dispute arising out of or in connection with this Agreement shall instead be resolved by arbitration under the Swiss Rules of International Arbitration of the Swiss Arbitration Centre in force when the notice of arbitration is submitted. The seat of the arbitration is Zurich, the arbitral tribunal consists of one arbitrator, and the language of the arbitration is English.

19.4 Blindsight may in any case apply for interim measures, or bring a claim for unpaid fees, before the competent courts at the Customer's seat.

**20. General**

20.1 This Agreement, the Service Terms, the DPA, the Customer's order and the file THIRD_PARTY_NOTICES.md are the entire agreement on their subject matter. If they conflict, the following order applies: (a) clause 6 of this Agreement, as far as the licence of a Third-Party Component requires; (b) any addendum under clause 17; (c) the DPA, for the processing of personal data; (d) a master agreement or order form signed by both parties; (e) the Service Terms and the Customer's order; (f) this Agreement; (g) the Documentation.

20.2 Neither party may assign this Agreement without the other party's prior written consent, which shall not be unreasonably withheld, except that either party may assign it to a successor to all or substantially all of its relevant business on written notice.

20.3 Notices under this Agreement must be in writing. Acceptance in the Blindsight console and e-mail to the addresses given by the parties satisfy this requirement. Amendments, other than new versions accepted under clause 18, require a document agreed by both parties in writing.

20.4 If a provision of this Agreement is invalid or unenforceable, the remaining provisions remain in force, and the invalid provision is replaced by a valid provision that comes closest to its purpose.

20.5 A failure or delay in exercising a right is not a waiver of it.

20.6 This Agreement is written in English. If it is translated, the English text prevails.
