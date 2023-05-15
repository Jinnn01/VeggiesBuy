//
//  UploadView.swift
//  VeggiesBuy
//
//  Created by Gabriel Komarnicki on 5/5/2023.
//

import SwiftUI

struct UploadView: View {
    
    @State private var vegetableName = ""
    @State private var vegetablePrice = ""
    @State private var vegetableUnit = ""
    @State private var supermarketName = ""
    @State private var supermarketLocation = ""
    @State private var showAlert = false // New state variable
    
    let marketName = ["ALDI", "Coles", "Woolworths"]
    
    @State private var selectedSupermarket = "ALDI"
    
    var body: some View {
        NavigationView {
            ZStack {
                Color.themeBackground
                    .edgesIgnoringSafeArea(/*@START_MENU_TOKEN@*/.all/*@END_MENU_TOKEN@*/)
                Form {
                    Section(header: Text("Vegetable details")) {
                        TextField("Vegetable Name", text: $vegetableName)
                        TextField("Vegetable Price", text: $vegetablePrice)
                        TextField("Vegetable Unit", text: $vegetableUnit)
                    }
                    Section(header: Text("Supermarket details")) {
                        TextField("Supermarket Name", text: $supermarketName)
                        /*
                        Picker("Supermarket Name:", selection: $selectedSupermarket) {
                            ForEach(marketName, id: \.self) {
                                Text($0)
                            }
                        }*/
                        TextField("Supermarket Location", text: $supermarketLocation)
                    }
                }
                .navigationBarTitle("Upload")
                .onTapGesture {
                    hideKeyboard()
                }
                .toolbar {
                    ToolbarItemGroup(placement: .navigationBarTrailing) {
                        Button("Save", action: saveVegItem)
                    }
                }
            }
        }
        .alert(isPresented: $showAlert) {
                    Alert(
                        title: Text("Item Saved"),
                        message: Text("Vegetable saved successfully!"),
                        dismissButton: .default(Text("OK"))
                    )
                }
    }
    
    func saveVegItem() {
        showAlert = true
                print("Vegetable item saved")
    }
}

struct UploadView_Previews: PreviewProvider {
    static var previews: some View {
        UploadView()
    }
}

// disable the keyboard when not in use
#if canImport(UIKit)
extension View {
    func hideKeyboard() {
        UIApplication.shared.sendAction(#selector(UIResponder.resignFirstResponder), to: nil, from: nil, for: nil)
    }
}
#endif
