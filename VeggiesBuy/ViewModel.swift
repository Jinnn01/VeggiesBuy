//
//  ViewModel.swift
//  VeggiesBuy
//
//  Created by Gabriel Komarnicki on 12/5/2023.
//

import Foundation
import SwiftUI

struct Vegetable1: Hashable, Codable {
    let sname: String
    let vname: String
    let price: Float
    let unit: String
    //let image: String
}


// iosacademy tutorial
class ViewModel1: ObservableObject {
    @Published var vegetables: [Vegetable1] = []
    
    //http://localhost:5000/api/items
    func fetch() {
        //guard let url = URL(string: "https://iosacademy.io/api/v1/courses/index.php") else {
            //return
        guard let url = URL(string: "http://localhost:5005/item") else {
            return
        }
        
        let task = URLSession.shared.dataTask(with: url) { [weak self] data, _,
            error in
            guard let data = data, error == nil else {
                return
            }
            
            // convert to JSON
            do {
                let vegetables = try JSONDecoder().decode([Vegetable].self, from: data)
                DispatchQueue.main.async {
                    //self?.vegetables = vegetables
                }
            }
            catch {
                print(error)
            }
        }
        task.resume()
    }
}
