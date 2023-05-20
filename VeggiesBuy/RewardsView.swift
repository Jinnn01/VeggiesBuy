//
//  RewardsView.swift
//  VeggiesBuy
//
//  Created by Gabriel Komarnicki on 7/5/2023.
//

import SwiftUI

struct RewardsView: View {
    
    @State private var item1 = ""
    @State private var item2 = ""
    @State private var item3 = ""
    
    var body: some View {
        NavigationView {
            
            ZStack {
                
                Form {
                    TextField("Item 1", text: $item1)
                    TextField("Item 2", text: $item2)
                    TextField("Item 3", text: $item3)
                }
            }
            .navigationBarTitle("Rewards")
        }
    }
}

struct RewardsView_Previews: PreviewProvider {
    static var previews: some View {
        RewardsView()
    }
}
